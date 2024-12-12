class SpamFilter:
    PROMOTIONAL_KEYWORDS = {
    "limited offer", "exclusive deal", "buy now", 
    "discount", "promo code", "act fast", "click to buy", 
    "guaranteed", "lowest price", "sale", "special offer",
     "money back", "risk free", "winner", "claim now",
    "no obligation", "free gift", "once in a lifetime",
    "don’t miss", "instant access", "congratulations", "get rich", 
     "double your", "secret trick", "as seen on",
    "unbelievable offer", "lose weight", "miracle cure", "easy money",
    "earn instantly", "limited spots", "hidden fees", "fake testimonials", "limited quantity",
    # Newly appended words and phrases
    "exclusive deal", "limited time only", "buy one, get one free", 
    "lowest price guaranteed", "save big", "act now", "today only", 
    "flash sale", "clearance", "don’t miss out", "hurry", "only a few left", 
    "while supplies last", "ends soon", "limited stock", "free gift", 
    "no cost", "complimentary", "sign up and save", "claim your prize", 
    "enter to win", "earn money fast", "make $1000 a week", "passive income", 
    "get rich quick", "no investment required", "click here", "see for yourself", 
    "guaranteed satisfaction", "risk-free trial", "as seen on TV", "best on the market", 
    "proven results", "revolutionary", "top-rated", 
    "lose weight fast", "anti-aging miracle", "cure-all solution", 
    "get flawless skin", "boost your energy"
}

    @classmethod
    def detect_promotional_content(cls, content: str) -> bool:
        """
        Detect if the content contains promotional or marketing keywords.
        """
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in cls.PROMOTIONAL_KEYWORDS)