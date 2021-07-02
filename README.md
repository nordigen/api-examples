# Flask example

This is official python library for [Nordigen](https://nordigen.com/).

For a full list of endpoints and arguments, see the [docs](https://nordigen.com/en/account_information_documenation/api-documention/overview/
).

### Install & run

You'll need to get your access token from the [Nordigen's Open Banking Portal](https://ob.nordigen.com/login/). In <strong>app.py</strong> file provide the token as a parameter for <strong>api.ng_token</strong>, and a two-letter country code as a parameter for <strong>api.country</strong> that will determine available banks (ASPSPs). 

```bash
pip3 install -r requirements.txt;
python3 app.py
```


##### 1. Go to http://localhost:8081/ and select bank
<!-- ![acc token](/docs/resources/_media/f_3_select_aspsp.png?raw=true "Title") -->
<p align="center">
    <img align="center" src="/docs/resources/_media/f_3_select_aspsp.png" width="200" />
</p>

##### 2. Provide consent
<p align="center">
  <img src="/docs/resources/_media/f_4_ng_agreement.jpg" width="200" />
  <img src="/docs/resources/_media/f_4.1_ng_redirect.png" width="200" /> 
</p>

##### 3. Sign in the bank (ASPSP)
<p align="center">
  <img src="/docs/resources/_media/f_5_aspsps_signin.png" width="230" />
  <img src="/docs/resources/_media/f_5.1_aspsps_signin.jpg" width="200" /> 
  <img src="/docs/resources/_media/f_5.2_aspsps_signin.jpg" width="200" /> 
</p>

<p align="center">
  <img src="/docs/resources/_media/f_5.3_aspsp_auth.jpg" width="200" /> 
</p>

##### 4. Select accounts
<p align="center">
  <img src="/docs/resources/_media/f_6_aspsp_accs.jpg" width="200" />
</p>

##### 5. Download data
Here a redirect from Nordigen to http://localhost:8081/results?ref={ref_id} happens
<p align="center">
  <img src="/docs/resources/_media/f_7_accc_data.png" width="500" />
</p>
