"""
Telegram alerting system for Chrysalis
"""
import requests
from typing import Optional
import logging
from chrysalis.config import config

logger = logging.getLogger(__name__)


class TelegramAlerter:
    """Send alerts via Telegram bot"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or config.telegram_bot_token
        self.chat_id = chat_id or config.telegram_chat_id
        
    def send_alert(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send alert message via Telegram
        
        Args:
            message: Alert message to send
            parse_mode: Message parse mode (HTML or Markdown)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram bot token or chat ID not configured")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Telegram alert sent successfully: {message[:50]}...")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram alert: {e}")
            return False
    
    def send_emergency(self, system: str, error: str, context: dict = None) -> bool:
        """
        Send emergency alert with structured format
        
        Args:
            system: System name (e.g., "Decision Cortex")
            error: Error description
            context: Additional context data
            
        Returns:
            bool: True if successful, False otherwise
        """
        context_str = ""
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        
        message = f"""
🚨 <b>CHRYSALIS EMERGENCY ALERT</b> 🚨

<b>System:</b> {system}
<b>Error:</b> <code>{error}</code>

<b>Context:</b>
<pre>{context_str}</pre>

<b>Action Required:</b> Immediate investigation needed.
"""
        return self.send_alert(message)


# Global instance
telegram_alerter = TelegramAlerter()