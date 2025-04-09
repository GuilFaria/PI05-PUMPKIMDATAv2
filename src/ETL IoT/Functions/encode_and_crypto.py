import hashlib
import base64
import io


#/------------------------Codificação------------------------/


def codifica_base64(content: list | io.BytesIO | str  = str) -> list[str] | str:

    '''
    Codificação de BASE64 é feito da seguinte forma(Número não exclusivo, apenas uma máscara):
    '''
    
    if isinstance(content, str):
        try:
            content = content.encode() #Para transformar em uma string correta, utiliza-se o decode no final
            encoded_value = base64.b64encode(content).decode()
        
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
                
            
    elif isinstance(content, io.BytesIO):
        try:
            encoded_value = base64.b64encode(content).decode()
        
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
            
    elif isinstance(content, list):
        try:            
            encoded_value = []
            for text in content:
                text = str(text)
                text_encoded = text.encode()
                based_text = base64.b64encode(text_encoded).decode()
                encoded_value.append(based_text)

        except Exception as e:
            raise(f'Erro ao codificar: {e}')
    
    return encoded_value




def decodifica_base64(content: list | io.BytesIO | str = str) -> list[str] | str:
    '''
    Decodificação de BASE64 é feito da seguinte forma(Número não exclusivo,
    apenas uma máscara):
    '''
    if isinstance(content, str):
        try:    
        
            content = content.encode()
            decoded_value = base64.b64decode(content).decode()
            
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
                
            
    elif isinstance(content, io.BytesIO):
        try:
            decoded_value = base64.b64decode(content).decode()
        
        except Exception as e:
            raise(f'Erro ao codificar: {e}')
            
    elif isinstance(content, list):
        try:            
            decoded_value = []
            for text in content:
                text = str(text)
                text_encoded = text.encode()
                based_text = base64.b64decode(text_encoded).decode()
                decoded_value.append(based_text)

        except Exception as e:
            raise(f'Erro ao codificar: {e}')
    
    return decoded_value


#/------------------------Criptografia------------------------/


def encriptografa_sha3_256(content: list | io.BytesIO | str= str) -> list[str] | str: 
    '''Criptografia de sha3-256 é feito da seguinte forma (Número EXCLUSIVO, sempre diferente)'''
    
    if isinstance(content, str):
        hash_text = content.encode()
        hash = hashlib.sha3_256(hash_text)
        return hash.hexdigest()
        
    elif isinstance(content, io.BytesIO):
        hash = hashlib.sha3_256(content)
        return hashs_list.hexdigest()
        
    elif isinstance(content, list):
        hashs_list = []
        for string in content:
            string = str(string)
            encoded_text = string.encode()
            hashed_text = hashlib.sha3_256(encoded_text).hexdigest()
            hashs_list.append(hashed_text)
        return hashs_list