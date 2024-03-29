# watch-ecommerce
This is an end to end eCommerce website built using Flowbite(for Tailwind css), Vanilla Javascript, Django Framework.
Integrated with payment APIs; Stripe and Daraja API(M-pesa).
We have used a PostgreSQL serverless database to enhance scalability and reliability.


## Required Software
- [Python 3.10](https://www.python.org/downloads/) or newer
- [Node.js 18.15 LTS](https://nodejs.org/) or newer (For Tailwind.CSS)
- [Git](https://git-scm.com/)


## Getting Started

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/gerald77-droid/watch-ecommerce-website
cd micro-ecommerce
git checkout start
```



_macOS/Linux Users_
```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install pip pip-tools rav --upgrade
venv/bin/rav run installs
rav run freeze
```


_Windows Users_
```powershell
c:\Python310\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip pip-tools rav --upgrade
rav run win_installs
rav run win_freeze
```
