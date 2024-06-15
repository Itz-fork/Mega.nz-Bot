# Megatools dev notes
Developer notes to work with mega.nz api

### Requesting nodes of a shared node
**Request:** Please refer to [`megatools.get_info`](/megatools.py?L=160)
**Response:**
```json
[
    {
        "h": "sysQhDbK",
        "p": "V6V01DBB",
        "u": "TnKrSNAJt4U",
        "t": 1,
        "a": "bnsrEUjW2A5gNe1qXiiQ_oySfftOThPhiowtaoU5T48",
        "k": "sysQhDbK:QXelBbZDeCYXN-M_Pu7VkQ",
        "ts": 1700099874,
    },
    ...
]
```
**Meaning:**
- "h": This is the handle ID of the file or folder. It's a unique identifier used by Mega.nz to refer to this specific file or folder.
- "p": This is the parent handle ID, which is the handle ID of the parent folder that this file or folder resides in.
- "u": This is the owner's user handle ID. It's a unique identifier for the user who owns this file or folder.
- "t": This is the type of the node. 0 means it's a file, 1 means it's a folder.
- "a": This is the attributes of the file or folder, which are encrypted. It usually contains the name of the file or folder after decryption.
- "k": This is the encrypted key of the file or folder. It's used to decrypt the file or folder's data.
- "s": This is the size of the file in bytes. It's not present if the node is a folder.
- "ts": This is the timestamp when the file or folder was last modified. It's in Unix time format (seconds since 1970-01-01 00:00:00 UTC).


**Example:**

```py
url = "https://mega.nz/folder/kyVnRBTC#LNLkMU1XRSlgds9dmtricA"
async with ClientSession() as session:
    params = {"id": 0, "n": root_folder}
    data = json.dumps(data)
    async with session.post("https://g.api.mega.co.nz/cs", params=params, data=data) as resp:
        nodes = (await resp.json())[0]["f"]
```
```json
[
    {
        "h": "sysQhDbK",
        "p": "V6V01DBB",
        "u": "TnKrSNAJt4U",
        "t": 1,
        "a": "bnsrEUjW2A5gNe1qXiiQ_oySfftOThPhiowtaoU5T48",
        "k": "sysQhDbK:QXelBbZDeCYXN-M_Pu7VkQ",
        "ts": 1700099874,
    },
    {
        "h": "xmt0EYSB",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "l-bKSQqGAE2TNV9IY1BM_toJc_CLLTAxmD1X_O9roNwzpaaj7V6d7x04eKCWE8IXgSE2-nolNc587JOcWoIymQ",
        "k": "sysQhDbK:i4AffLKntCDlSttMmehcOynL5G8JyERenLpg99AeX6s",
        "s": 13122,
        "fa": "890:1*VZQRRp1QKYI/890:0*CQL62liSrUI",
        "ts": 1700101974,
    },
    {
        "h": "MjMTVbJS",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "KQYy1iBboKogMuTmJdVmbiQqktBlc2w0pQnKARE8HUs",
        "k": "sysQhDbK:JnFnmmshH15OLYl6FXZMqBoVffh6KUDb3qrZa5cyWTg",
        "s": 1593497,
        "ts": 1700329169,
    },
    {
        "h": "hrcGyLbY",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "Pm7H0Dnv_CmJ8ez821kWNt0NaM9-ZT78ayJPQMrH52A",
        "k": "sysQhDbK:dPId-z-aap5LocAUmX98dkQuddbpDlahLJ-zWf1VoB4",
        "s": 1593497,
        "ts": 1700329639,
    },
    {
        "h": "Jjsy0LKY",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "oCCVXOeJlgxTIlyk8hz6qs2h1DB2lJF4o-FBXwKCkWfhfLX8Ci53G2a1QLBuBVsdY3Vt1nzSXkvw2bdbg8YTIA",
        "k": "sysQhDbK:njevAZbQbP3cuRMfROwvA8vwLiFNJdATqdPX5rw7ayI",
        "s": 1593497,
        "ts": 1700329763,
    },
    {
        "h": "JvMQFRIK",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "KR3smaRfDHQ_XRpOLdn_e9slaxe_zYqsfWcPT7gInSW-oDYS0kc_ELZJwY61BkffdGEVXrfNPFrfKWtBH95yLw",
        "k": "",
        "s": 80299,
        "ts": 1703303819,
    },
    {
        "h": "B70kHJiA",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "ohhUSw5SoCGX_KPpfOe-KNxBI5e_ArNxxtqxgRQzMF0",
        "k": "",
        "s": 309868,
        "ts": 1703357584,
    },
    {
        "h": "QzUAHZaT",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "CLwNRF1cRA4gi2uakRpsXmsdQbOCMl6bnAQpI0JeihM",
        "k": "",
        "s": 29380545,
        "ts": 1703404548,
    },
    {
        "h": "1q1FVQhB",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "v5w0IeXk1oZU2Y3iORtULh2294FGfmWH4cpesAzaN-9vAbF1Ro1yOhy-JVDuDb_78zbNQqgbmQNBK2SSUYTllA",
        "k": "",
        "s": 119919,
        "ts": 1703533602,
    },
    {
        "h": "4mUV0RxJ",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "yAKkfAaM73MF4DAceYuPgQTrNFX-ScwH5PGi6usJ9sE",
        "k": "",
        "s": 119919,
        "ts": 1703533697,
    },
    {
        "h": "QilC3CRS",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "2zGRb-uS-C-daouN6-JfqyONWf7PKYGOurlkNRHGE6b1SuAIrB-1znOu79Lr6SZ6I9dQsIQ0SiGIB2RJD_hgSw",
        "k": "",
        "s": 119919,
        "ts": 1703533756,
    },
    {
        "h": "pusxRKiQ",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "uxg0W-TGdyKwkWq0FaFkUf7cp9jLvC4rA5e1SRmRmtd2gbw13rKZCrbuRdArO_ZejNlRKjLs28HnLfJS1G7Bfg",
        "k": "",
        "s": 119919,
        "ts": 1703533823,
    },
    {
        "h": "0zkyBRQB",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "zYoorHD9IZNt_JimVQLW2dFu4MWaoi5oqZteYf2m84FwKZ_IvCIduPiOp_EQ-Vtex3ly8g-t819LWfeHe9L35g",
        "k": "",
        "s": 119919,
        "ts": 1703595696,
    },
    {
        "h": "Q2kC3ahT",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "e8GCdzo9sWek5bMZwRPV5R9eX3f9euzVKnw_47NwCCU",
        "k": "",
        "s": 119919,
        "ts": 1703608309,
    },
    {
        "h": "d69mHJaQ",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "VqNaP8wP6r7Lq7itjJeQ2tywbzhd33SYv7KNzNFLbEddFy2jgPyfEEJv-Ki0PsfwVdcw2In9esL-SS76NgZdbw",
        "k": "",
        "s": 119919,
        "fa": "115:0*ZxoCHoZin7w",
        "ts": 1703870835,
    },
    {
        "h": "Z6tXQbZD",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "-NQnlI_wgBq5SDuDN9nvqM8DzIk7LAI3eDKdSnr5jQQ4CzWnf0P8Zw0ajiOsaJf2LTSyEPYM_KYT5WOFPRq3zw",
        "k": "",
        "s": 119919,
        "fa": "700:0*hJxqzZ4BN8s",
        "ts": 1703871085,
    },
    {
        "h": "wvFRADiK",
        "p": "sysQhDbK",
        "u": "TnKrSNAJt4U",
        "t": 0,
        "a": "4W0R8WSdUCGkyU610L6w_ohceu_X6dZBbm7DY61Nzc6zR3wzJFDOkJvqhkpV0Au1t0vCkFANikUlSmOJ3-r9MQ",
        "k": "",
        "s": 16832,
        "fa": "701:0*mDTZFNtqpG8",
        "ts": 1703873565,
    },
]
```