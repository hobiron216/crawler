import requests

cookies = {
    'tuuid': 'b560270b-45e8-445d-b00a-d499306d961f',
    'c': '1605512545',
    'tuuid_lu': '1613366296',
}

headers = {
    'authority': 'googleads.g.doubleclick.net',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cookie': 'RUL=EOLz8P4FGOLa9Y0GIqECATZhkOMeBDqpr3jXv2up8fpasKozZrhHWXnoAXurt3tJuNT2EF-DhNXk_ByR04HMN94tMzz70X4sd9dFkBFWrRl1UqCqk8Gnvmr5dBmA9EUWTT8cMpXzpm3UPa4t-K0wrXpsSUARWc0j8YgJpKmxeGTx6RFneCAzQqLWg2eoertw8R2y-tNc50isbXvTxFcXq9X_L79aqw6rRx1PBKLsbYkDVg7cc8H06GyggX4Jm7b2Tcx4TNvVAkKdrvMVQoEkRafBCVtDetPcJ1ePYRwQxjy7Ih1gqFN9qQKcf3PFYCc9_yvk5o74F0XML0ztrhPVnHDp3rUCcHxQM0lzUNmltfCFeifpCtzG7G0TYyM4PdMH9gAaYCf0NMiHWfXZKj_Tew|cs=AP6Md-UgGuzkM6BzxMtncw9ouZ9U; IDE=AHWqTUk_B-QHKOUFGbEY2xw4IHD3uPm4wVuOfAHc-pET4CAf2MFnG68IHCoA0qa0kLY; DSID=AAO-7r5BH5W5_FQaDB9w81ZvFOx_-SitTpfOGvS1pJzGVZgi5r8bLy0y6UgBvlS-6iLA_UeDt-FTVytSamdmCsJHChmKF_pc88p2ctqnchCNjUZg2ewixg8',
    'Referer': 'https://tpc.googlesyndication.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'referer': 'https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-4019842536198161&output=html&h=600&slotname=3789905075&adk=3871965213&adf=3407277730&pi=t.ma~as.3789905075&w=160&fwrn=3&psa=1&format=160x600&url=https%3A%2F%2Fwww.kwongwah.com.my%2F%2Fcategory%2F%25E5%259B%25BD%25E5%2586%2585%25E6%2596%25B0%25E9%2597%25BB%2Fpage%2F471&ea=0&flash=0&wgl=1&dt=1614935939066&bpp=36&bdt=259&idt=611&shv=r20210303&cbv=r20190131&ptt=9&saldr=aa&cookie=ID%3D146824442ac55a65%3AT%3D1614935542%3AS%3DALNI_MbxlBdE8qnd-SXGNy29cwPpNXRtnA&correlator=2586066443772&frm=23&ife=4&pv=2&ga_vid=332776543.1614329472&ga_sid=1614935940&ga_hid=1011317562&ga_fc=1&nhd=2&u_tz=420&u_his=6&u_java=0&u_h=864&u_w=1536&u_ah=824&u_aw=1536&u_cd=24&u_nplug=3&u_nmime=4&adx=-12245933&ady=-12245933&biw=637&bih=754&isw=0&ish=0&ifk=1278228171&scr_x=0&scr_y=0&eid=31060287%2C21068084&oid=2&pvsid=194048339770021&pem=667&rx=0&eae=2&fc=640&brdim=0%2C0%2C0%2C0%2C1536%2C0%2C1536%2C824%2C0%2C0&vis=1&rsz=%7C%7CEr%7C&abl=CS&pfx=0&fu=8196&bc=31&ifi=1&uci=1.enyv3oviupda&fsb=1&dtd=1016',
    'Intervention': '<https://www.chromestatus.com/feature/5718547946799104>; level="warning"',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Origin': 'https://www.kwongwah.com.my',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'image',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'content-length': '0',
    'content-type': 'text/plain',
    'origin': 'https://www.kwongwah.com.my',
    'x-client-data': 'CIW2yQEIpLbJAQjEtskBCKmdygEI+MfKAQikzcoBCNnPygEI3NXKAQjGnMsBCOScywEIqZ3LAQ==',
    'purpose': 'prefetch',
    'Upgrade-Insecure-Requests': '1',
    'cache-control': 'max-age=0',
}

response = requests.get('https://www.kwongwah.com.my//category/%E5%9B%BD%E5%86%85%E6%96%B0%E9%97%BB/page/471', headers=headers)
print(response.text)