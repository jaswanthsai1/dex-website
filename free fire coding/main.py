import requests, os, sys, jwt, json, time, urllib3
import socket, threading
from me import *
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import xKEys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

K  = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
Iv = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

tPl = bytes.fromhex('1a13323032362d30312d31342031313a35383a3037220966726565206669726528013a07312e3132302e30423a416e64726f6964204f532039202f204150492d32382028505133422e3139303830312e31303130313834362f47393635305a48553241524336294a0848616e6468656c645207566572697a6f6e5a045749464960800f68b80872033238307a2141524d3634204650204153494d442041455320564d48207c2032383635207c20348001bb178a010f416472656e6f2028544d29203634309201134f70656e474c20455320332e312076312e34369a012b476f6f676c657c33346137646364662d613764352d346362362d386437652d336230653434386130633537a2010d3232332e3139312e35312e3839aa0102656eb201203433303632343537393364653836646134323561353263616164663231656564ba010134c2010848616e6468656c64ca010430374051ea014034653739616666653331343134393031353434656161626562633437303537333866653638336139326464346335656533646233333636326232653936363466f00101ca0207566572697a6f6ed2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e0038b9b02e803e7f401f003d713f803bf058004b2c301880484d0019004e0810298048b9b02c80403d2043f2f646174612f6170702f636f6d2e6474732e667265656669726574682d59504b4d386a484577414a6c68706d68446876354d513d3d2f6c69622f61726d3634e00401ea045f35623839326161616264363838653537316636383830353331313861313632627c2f646174612f6170702f636f6d2e6474732e667265656669726574682d59504b4d386a484577414a6c68706d68446876354d513d3d2f626173652e61706bf00403f804028a050236349a050a32303139313138363935b205094f70656e474c455332b805ff7fc00504ca0530467751565467555058315561556c6c4444776357435242705741554f556773764131736e576c42614f316b4659673d3de005fc69ea0507616e64726f6964f2055c4b71734854796d77352f354742323359476e6955594e322f71343747415472713765466552617466304e6b774c4b454d5130504b35424b456b37326450666c4178556c454269723656746579383358714635393371736c386877593df805b9db068806019006019a060134a2060134')

iNuRl = "https://100067.connect.garena.com/oauth/token/inspect?token={t}"
iNhDr = {"Accept-Encoding":"gzip, deflate, br","Connection":"close","Content-Type":"application/x-www-form-urlencoded","Host":"100067.connect.garena.com","User-Agent":"GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"}
mLuRl = "https://loginbp.ggwhitehawk.com/MajorLogin"
mLhDr = {"X-Unity-Version":"2018.4.11f1","ReleaseVersion":"OB52","Content-Type":"application/x-www-form-urlencoded","X-GA":"v1 1","User-Agent":"Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)","Host":"loginbp.ggwhitehawk.com","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
gLuRl = "https://clientbp.ggwhitehawk.com/GetLoginData"
gLhDr = {"Expect":"100-continue","X-Unity-Version":"2018.4.11f1","X-GA":"v1 1","ReleaseVersion":"OB52","Content-Type":"application/x-www-form-urlencoded","User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)","Host":"clientbp.ggwhitehawk.com","Connection":"close","Accept-Encoding":"gzip, deflate, br"}

wElc = "[b][c][00f7f9]━━━━━━━━━━━━\n[C][B][FFFFFF]Tr1pLiX Bot\n[C][B][00f7f9]━━━━━━━━━━━━"

class Bot:
    def __init__(self, aT, n, tot):
        self.aT  = aT
        self.aId = None
        self.pSk = None
        self.sSk = None
        print(f"[{n}/{tot}] starting")
        self.run()

    def bLdPl(self, at, oid):
        t = tPl[:]
        t = t.replace(b'2026-01-14 14:11:20', str(datetime.now())[:-7].encode())
        t = t.replace(b'4e79affe31414901544eaabebc4705738fe683a92dd4c5ee3db33662b2e9664f', at.encode())
        t = t.replace(b'4306245793de86da425a52caadf21eed', oid.encode())
        return bytes.fromhex(EnC_AEs(t.hex()))

    def gAuth(self):
        r = requests.get(iNuRl.format(t=self.aT), headers=iNhDr, timeout=10).json()
        if 'error' in r: raise Exception(f"inspect: {r.get('error')}")
        oid = r['open_id']
        pl  = self.bLdPl(self.aT, oid)
        x   = requests.post(mLuRl, headers=mLhDr, data=pl, verify=False, timeout=15)
        if not x.ok: raise Exception(f"MajorLogin {x.status_code}")
        psd = json.loads(DeCode_PackEt(x.content.hex()))
        tok = psd['8']['data']
        if not tok: raise Exception("empty jwt")
        msg = xKEys.MyMessage()
        msg.ParseFromString(x.content)
        ts  = Timestamp()
        ts.FromNanoseconds(msg.field21)
        tNs = ts.seconds * 1_000_000_000 + ts.nanos
        k, v = msg.field22, msg.field23
        cl   = jwt.decode(tok, options={"verify_signature": False})
        self.aId = cl.get('account_id')
        gH  = {**gLhDr, "Authorization": f"Bearer {tok}"}
        r2  = requests.post(gLuRl, headers=gH, data=pl, verify=False, timeout=12)
        if r2.status_code != 200: raise Exception(f"GetLoginData {r2.status_code}")
        srv = json.loads(DeCode_PackEt(r2.content.hex()))
        a1  = srv['32']['data']
        a2  = srv['14']['data']
        return tok, k, v, tNs, a1[:len(a1)-6], a1[len(a1)-5:], a2[:len(a2)-6], a2[len(a2)-5:]

    def gPkt(self, tok, k, v, ts):
        e  = EnC_PacKeT(tok.encode().hex(), k, v)
        hx = hex(int(self.aId))[2:]
        ln = len(hx)
        pd = '0000000' if ln==9 else '000000' if ln==10 else '000000000' if ln==7 else '00000000'
        return f"0115{pd}{hx}{DecodE_HeX(ts)}00000{hex(len(e)//2)[2:]}{e}"

    def snd(self, msg, t, s, r, k, v):
        try: self.pSk.send(xSEndMsg(msg, t, s, r, k, v))
        except: pass

    def sLp(self, ip, port, auth):
        while True:
            try:
                self.sSk = socket.create_connection((ip, int(port)))
                self.sSk.send(bytes.fromhex(auth))
                while True:
                    d = self.sSk.recv(99999)
                    if not d: break
            except: time.sleep(2)

    def lp(self, tok, k, v, ip1, p1, ip2, p2):
        while True:
            try:
                d = self.pSk.recv(1024)
                if not d: break
                hx = d.hex()
                if '1200' in hx[0:4] and 100 < len(hx) < 900:
                    if b"***" in d: d = d.replace(b"***", b"106")
                    try:
                        dec = json.loads(DeCode_PackEt(hx[10:]))
                        cid = dec["5"]["data"]["1"]["data"]
                        self.snd(wElc, 2, cid, cid, k, v)
                    except: pass
            except: break
        self.rCon(tok, k, v, ip1, p1, ip2, p2)

    def cOn(self, tok, k, v, tNs, ip1, p1, ip2, p2):
        auth = self.gPkt(tok, k, v, tNs)
        self.pSk = socket.create_connection((ip1, int(p1)))
        self.pSk.send(bytes.fromhex(auth))
        self.pSk.recv(1024)
        print(f"connected {str(self.aId)[:8]}")
        threading.Thread(target=self.sLp, args=(ip2, p2, auth), daemon=True).start()
        self.lp(tok, k, v, ip1, p1, ip2, p2)

    def rCon(self, tok, k, v, ip1, p1, ip2, p2):
        for sk in (self.pSk, self.sSk):
            try: sk.close()
            except: pass
        print(f"reconnecting {str(self.aId)[:8]}")
        time.sleep(2)
        self.cOn(tok, k, v, 0, ip1, p1, ip2, p2)

    def run(self):
        try:
            tok, k, v, tNs, ip1, p1, ip2, p2 = self.gAuth()
            self.cOn(tok, k, v, tNs, ip1, p1, ip2, p2)
        except Exception as e:
            print(f"err: {e}")

def gToks():
    toks = []
    print("="*48)
    while True:
        t = input("Access Token --> ").strip()
        if t: toks.append(t)
        if input("Add another? (y/n) --> ").strip().lower() != 'y': break
    print(f"loaded {len(toks)}")
    return toks

def main():
    toks = gToks()
    if not toks: print("no accounts"); return
    print(f"starting {len(toks)}")
    for i, t in enumerate(toks, 1):
        time.sleep(1)
        Bot(t, i, len(toks))

if __name__ == "__main__":
    main()
