import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ecommerce.log"), # has a secoond argument mode = 'a' (default)
        logging.StreamHandler()  
    ]
)

logger = logging.getLogger("ecommerce")
