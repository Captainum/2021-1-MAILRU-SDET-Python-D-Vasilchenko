class ResponseHandler:
    @staticmethod
    def handle(response):
        ret = {'code': None, 'headers': {}, 'data': ''}
        data = False
        for i in range(len(response)):
            if i == 0:
                ret['code'] = int(response[i].strip().split()[1])
            if response[i] == '':
                if i == len(response) - 1:
                    break
                else:
                    data = True
            
            if not data:
                parsed = response[i].strip().split()
                
                header = parsed[0].split(':')[0]
                value = parsed[1]
                
                ret['headers'][header] = value            
            else:
                ret['data'] += response[i].strip()

        return ret