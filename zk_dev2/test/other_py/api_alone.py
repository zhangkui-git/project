import requests
import sys


class Test1(object):
        url = "https://192.168.4.249:8440/login/userLogin"
        headers = {"Content-Type": "application/json"}
        body = {"userName":"ewQB5138ITr39h2RyCEBErn0gtZOHkmKq0skZr8pQrtI/epRT5wZ4N7wGhL3ygkvfmGlOPZ74jmKlpFierp+3VFrH2vGG7Pal7uUxMa4STOdcfSdptHG9t5xQfp1zcSsyMC6zjwmLIq9RjuKi8ACT1TLkSyekhi30HAN0CiZqPDbNk3FjA2muyXgU/zpZdUZ3HH/l5/tiPHzIAwNVkNuwEujEvA064LaW1ndIXQmjvK0YZw4hxQbT/ZDyVI7UHrOKirFtxychDLqeJSIRBrSsZQ1MdX8vM3XcJvgi1fstF5GJYv1TQSNYnOKW6fNw6GdWR2m9ZzyvtE18w9L/gA+0w==","userPassword":"UNMK46amDQja58Rqz1MjUE2yAgasEUrfPEmiPvhmS06nehbKyaf7xOCkVF43LdhbdRETC5KJgHXG+zDcGMGeuaGN70ShWRtwCRvOe7KaDIOAZP7IOGfixQX8EFGvYM7xs4uwjpYTb6BzyxommerPZpWSdJNDt91mgDGj3LElOZx3Ah+ZuL1sLRSvhQAM0CrdKKIfrXKnL2zI1fzoX2SplpWWS4sWm1nnxfWqSMkjbxu2fLIKuUcz3iPjXCrI+CjIaCvDQWvEPoQq3h+O9vr6XOMQVY8XGdDWii2H5iKLiPklohMlSw1VMfIwuTFV479uyYqL71H8B47BeL8A5nGVdA=="}
        res = requests.post(url=url, headers=headers, json=body, verify=False)
        print("00000000000", f"{res.json()['data']['accessToken']}")
        token = res.json()['data']['accessToken']

        def create_file(num):
                create_file_url = "https://192.168.4.249:8440/assets/confirm"
                create_file_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{Test1.token}'}
                # create_file_body = {"ssoUsers":[],"ip":"192.168.41.10","name":"test1-10","modelId":"","factoryId":3,"mac":"","alias":"","serialNumber":"","deviceVersion":"","hasGuard":"","operateSystem":"","ipMacs":[],"typeId":"","vendorId":"","belongingUnit":"","belongProfessiona":"","belongingSystem":"","hostName":"","physicalPortNumber":"","loginTime":"","assetBusinessValue":"3","assetConfidentiality":"","assetIntegrity":"","assetAvailability":"","safetyResponsiblePerson":"","values":[""],"ssoType":"","ssoVersion":"","ssoAddr":""}
                create_file_body = {"ssoUsers":[],"ip":f"192.168.41.{num}","name":f"test1-{num}","modelId":"","factoryId":3,"mac":"","alias":"","serialNumber":"","deviceVersion":"","hasGuard":"","operateSystem":"","ipMacs":[],"typeId":"","vendorId":"","belongingUnit":"","belongProfessiona":"","belongingSystem":"","hostName":"","physicalPortNumber":"","loginTime":"","assetBusinessValue":"3","assetConfidentiality":"","assetIntegrity":"","assetAvailability":"","safetyResponsiblePerson":"","values":[""],"ssoType":"","ssoVersion":"","ssoAddr":""}
                create_file_res = requests.post(url=create_file_url, headers=create_file_headers, json=create_file_body, verify=False)
                print(create_file_res.json())


if __name__ == '__main__':
    Test1.create_file(91)






