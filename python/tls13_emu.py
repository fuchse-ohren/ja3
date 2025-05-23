def ja3_tls13(ja3_text):
    buff = ja3_text.split(",")
    # JA3の場合
    if len(buff) == 5:
        #クライアント側はTLS1.2との互換性維持のために振る舞いがあまり変化しない
        
        [v,c,e,ec,ecp] = buff

        # TLSバージョンを771で固定(RFC8446)
        v = "771"

        # Cipher Suitesには手を加えない(TLS1.2互換のために古いものも含まれるため)
        c = c

        # Extensionsには43-45-51-27-21を追加
        e = e.split("-")
        for i in ['43','45','51','27','21']:
            if i not in e:
                e.append(i)
        e = "-".join(e)

        # ECには触れない
        ec=ec
        ecp=ecp

        return ",".join([v,c,e,ec,ecp])

    # JA3Sの場合
    if len(buff) == 3:
        [v,c,e] = buff
        
        # TLSバージョンを771で固定(RFC8446)
        v = "771"

        # Cipher Suiteには手を加えない(矛盾点)
        c = c

        # Extensionsは43,41,51以外を削除
        e = e.split("-")
        rm = []
        for k in range(len(e)):
            if e[k] not in ['43','41','51']:
                rm.append(e[k])
        for i in rm:
            e.remove(i)

        #51もしくは41は必須
        if '51' not in e and '41' not in e:
            e.append('51')

        #43は必須
        if '43' not in e:
            e.append('43')
        
        e = "-".join(e)
        
        return ",".join([v,c,e])

if __name__ == '__main__':
    ja3 = "769,47–53–5–10–49161–49162–49171–49172–50–56–19–4,0–10–11,23–24–25,0"
    ja3s = "769,47,65281–0–11–35–5–16"
    print('テスト1 JA3')
    print(f"\tオリジナル: {ja3}")
    print(f"\tTLS1.3再現: {ja3_tls13(ja3)}")

    print('テスト2 JA3S')
    print(f"\tオリジナル: {ja3s}")
    print(f"\tTLS1.3再現: {ja3_tls13(ja3s)}")
