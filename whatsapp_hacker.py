"""
WhatsApp Message Interceptor - BUGGY CODE CHALLENGE
====================================================
Este código tenta interceptar e processar mensagens do WhatsApp,
mas contém varios bugs que precisam ser corrigidos.

OBJETIVO: Encontre e corrija todos os 5 bugs no código!
"""

import re
import json
from datetime import datetime
from typing import List, Dict

class WhatsAppHacker:
    def __init__(self, message_log_file: str):
        self.message_log_file = message_log_file
        self.messages = []
        self.encrypted_messages = {}
    
    def load_messages(self) -> List[Dict]:
        """Carrega mensagens do arquivo de log"""
        try:
            with open(self.message_log_file, 'r') as f:
                data = json.load(f)
                # BUG 1: Tentando acessar 'messages' mas o JSON pode ter outra estrutura
                self.messages = data['messages']
                return self.messages
        except FileNotFoundError:
            print(f"Arquivo {self.message_log_file} não encontrado")
            return []
    
    def extract_phone_numbers(self) -> List[str]:
        """Extrai números de telefone das mensagens"""
        phone_numbers = []
        # BUG 2: Regex incompleto - não captura todos os formatos
        pattern = r'\+55\s?\d{2}\s?\d{4}'
        
        for message in self.messages:
            content = message.get('content', '')
            matches = re.findall(pattern, content)
            phone_numbers.extend(matches)
        
        return phone_numbers
    
    def decrypt_message(self, encrypted_msg: str, key: int) -> str:
        """Descriptografa mensagem usando shift cipher"""
        decrypted = ""
        # BUG 3: Loop infinito - falta incrementar o índice
        i = 0
        while i < len(encrypted_msg):
            char = encrypted_msg[i]
            if char.isalpha():
                shift = ord(char) - key
                decrypted += chr(shift)
            else:
                decrypted += char
            # FALTA: i += 1
        
        return decrypted
    
    def filter_messages_by_keyword(self, keyword: str) -> List[Dict]:
        """Filtra mensagens que contenham uma palavra-chave"""
        filtered = []
        # BUG 4: Comparação case-sensitive quando deveria ser case-insensitive
        for message in self.messages:
            if keyword in message['content']:
                filtered.append(message)
        
        return filtered
    
    def get_message_statistics(self) -> Dict:
        """Calcula estatísticas das mensagens"""
        if not self.messages:
            return {}
        
        total_messages = len(self.messages)
        # BUG 5: Divisão por zero quando não há mensagens
        average_length = sum(len(msg['content']) for msg in self.messages) / total_messages
        
        timestamps = [msg['timestamp'] for msg in self.messages]
        first_message = min(timestamps)
        last_message = max(timestamps)
        
        return {
            'total_messages': total_messages,
            'average_length': average_length,
            'first_message': first_message,
            'last_message': last_message
        }
    
    def process_all(self):
        """Processa todas as operações"""
        print("Carregando mensagens...")
        self.load_messages()
        
        print(f"Total de mensagens: {len(self.messages)}")
        
        print("\nExtraindo números de telefone...")
        phones = self.extract_phone_numbers()
        print(f"Telefones encontrados: {phones}")
        
        print("\nEstatísticas:")
        stats = self.get_message_statistics()
        print(json.dumps(stats, indent=2))


# Exemplo de uso
if __name__ == "__main__":
    hacker = WhatsAppHacker("messages.json")
    hacker.process_all()
