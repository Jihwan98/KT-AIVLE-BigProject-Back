# secret 정보 여기다가 모아둠
SOCIAL_INFO = {
    "SECRET_KEY":"django-insecure-u^dwaltg9ji$czy^1=z=d(6ue=(-b5pb316l$bhi5j*uxgu95b",
    "MAIN_DOMAIN":"http://127.0.0.1:8000",
    # "MAIN_DOMAIN":"http://43.202.5.122",
    "NAVER_CLIENT_ID":"IRgfKb5GJoBUhJb2xHFm",
    "NAVER_CLIENT_SECRET":"KIjZ6wTLF3",
    # KAKAO_REST_KEY
    "KAKAO_REST_API_KEY": "0e1fa375bb3d9b356f7ec7213157ccb0",
    "KAKAO_REDIRECT_URI":"http://127.0.0.1:8000/accounts/kakao/callback/",
     # GOOGLE
    "GOOGLE_CLIENT_ID": "375584534650-k59r41tkahfjikkq2r3qod42bis6851d.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "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",
     
    "STATE":"NAVER_LOGIN_STRING",
    "SOCIALACCOUNT_PROVIDERS":{
        "naver":{
            "APP":{
                "client_id":"IRgfKb5GJoBUhJb2xHFm",
                "secret":"KIjZ6wTLF3",
                "key":""
            }
        },
        # 카카오
        "kakao": {
            
        },
        # 구글
        'google' : {
            "APP": {
                "client_id": "375584534650-k59r41tkahfjikkq2r3qod42bis6851d.apps.googleusercontent.com",
                "secret": "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",
                "key": ""
            }
        },
        
        # -- 추가 예정 --
        # 구글
        # -- 추가 예정 -- 
    }
}
#http://127.0.0.1:8000/user/naver/callback?code=vO2xfQ1DWOXxSbH9n4&state=NAVER_LOGIN_STRING
