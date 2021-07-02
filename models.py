"""Nordigen API endpoints."""
import json
import uuid
from typing import Any

import requests
import settings


class Endpoints(object):
    """Nordigen API endpoints."""

    def __init__(self):
        """Variables used trough all api calls."""
        self.ng_token = None
        self.agreements = []
        self.enduser_id = None
        self.reference_id = None
        self.aspsp_id = None
        self.country = None
        self.requisition_id = None

    def _get_response(self, method: str, url: str, data: dict) -> Any:
        """
        Handle actual request to NG API.

        Args:
            method (str): Request method: GET | POST
            url (str): Request URL
            data (dict): GET payload or POST data

        Raises:
            HTTPError: On status code other than 200
            ValueError: on method other than GET, POST

        Returns:
            json: Response json
        """
        base_headers = {
            'accept': 'application/json',
            'Authorization': f'Token {self.ng_token}',
            'Content-Type': 'application/json'
        }

        method = method.upper()

        if method == 'GET':
            response = requests.get(url,
                                    headers=base_headers,
                                    params=data)
        elif method == 'POST':
            response = requests.post(url,
                                     headers=base_headers,
                                     data=json.dumps(data))
        else:
            raise ValueError(f"Unexpected method: {method}")

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            raise

        return response.json()

    def aspsps(self, country: str):
        """
        Get all available ASPSPs (banks) in a given country.

        Args:
            country (str): Two-character country code

        Returns:
            list: ASPSPs in given country
        """
        self.country = country
        payload = {'country': self.country}
        return self._get_response('GET', f'{settings.BASE_URL}/api/aspsps/', payload)

    @staticmethod
    def filter_aspsps(banks: list, filter_item: str) -> list:
        """
        Filter ASPSPs (banks) in a given country.

        Args:
            banks (list): List of all banks in a given country
            filter_item (str): search term for filtering

        Returns:
            banks (list): List of filtered banks in a given country
        """
        filter_item = filter_item.lower()
        return [a for a in banks if filter_item in a["name"].lower()]

    @staticmethod
    def add_logo_link(banks: list) -> list:
        """
        Get links for ASPSPs (banks) logos in a given country.

        Args:
            banks (list): List of all banks in a given country, returned in /api/aspsps/

        Returns:
            list: All banks and links to logos
        """
        with open(settings.CURRENT_DIR +
                  "/docs/resources/_data/logo_links.csv", 'r') as f:
            logo_links = dict(ln.strip().split(',', 1) for ln in f.readlines()[1:])

        for b in banks:
            b["logo_link"] = logo_links.get(
                b['id'], "https://static.thenounproject.com/png/95203-200.png"
            ).replace('"', '')

        return banks

    def enduser_agreement(self, aspsp_id: str, max_historical_days: int = 90):
        """
        Create end user agreement and add it to list of agreements.

        Args:
            aspsp_id (str): Unique identifier of the end-users' bank
            max_historical_days (int, optional): Length of the transaction history.
                                                 Defaults to 90.
        """
        self.aspsp_id = aspsp_id
        data = {
            'enduser_id': self.enduser_id,
            'max_historical_days': max_historical_days,
            'aspsp_id': self.aspsp_id
        }

        response_data = self._get_response(
            'POST', f'{settings.BASE_URL}/api/agreements/enduser/', data)
        self.agreements.append(response_data['id'])

    def requisitions(self):
        """Create requisition for creating links and retrieving accounts."""
        self.reference_id = str(uuid.uuid4())
        data = {
            'redirect': settings.REDIRECT_URL,
            'reference': self.reference_id,
            'enduser_id': self.enduser_id,
            'agreements': self.agreements
        }

        response_data = self._get_response(
            method='POST',
            url=f'{settings.BASE_URL}/api/requisitions/',
            data=data)
        self.requisition_id = response_data['id']

    def requisition_link(self) -> str:
        """
        Create a redirect link for the end user to ASPSP.

        Returns:
            str: Redirect link
        """
        data = {
            'aspsp_id': self.aspsp_id
        }
        response_data = self._get_response(
            method='POST',
            url=f'{settings.BASE_URL}/api/requisitions/{self.requisition_id}/links/',
            data=data
        )
        return response_data['initiate']

    def accounts(self) -> list:
        """
        List accounts.

        Returns:
            list: Accounts
        """
        response_data = self._get_response(
            method='GET',
            url=f'{settings.BASE_URL}/api/requisitions/{self.requisition_id}/',
            data=dict()
        )

        return response_data['accounts']

    def acc_data(self, accounts: list) -> dict:
        """
        Get account data - details, balances & transactions. Save data into json.

        Args:
            accounts (list): Account IDs

        Returns:
            dict: All accounts data
        """
        ret_dict = {}

        # Get details/balances/transactions for all accounts
        for acc in accounts:
            ret_dict[acc] = {}

            for url_path in ['details', 'balances', 'transactions']:
                response_data = self._get_response(
                    'GET', f'{settings.BASE_URL}/api/accounts/{acc}/{url_path}/', {}
                )

                # Save results
                with open(f'{settings.CURRENT_DIR}/downloads/{acc}_{url_path}.json',
                          'w') as save_file:
                    json.dump(response_data, save_file)

                ret_dict[acc][url_path] = response_data

        return ret_dict
