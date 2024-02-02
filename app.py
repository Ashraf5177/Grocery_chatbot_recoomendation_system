from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
app = Flask(__name__)

# Define some example category options with price and quantity information
category_options = {
    'freshvegetable': [
        {'name': 'onion', 'default_price': 25, 'default_quantity': 100, 'id': 'onion'},
        {'name': 'potato', 'default_price': 20, 'default_quantity': 100, 'id': 'potato'},
        {'name': 'tomato', 'default_price': 30, 'default_quantity': 100, 'id': 'tomato'},
        {'name': 'cauliflower', 'default_price': 40, 'default_quantity': 100, 'id': 'cauliflower'},
        {'name': 'carrot', 'default_price': 35, 'default_quantity': 100, 'id': 'carrot'},
        {'name': 'pea', 'default_price': 50, 'default_quantity': 100, 'id': 'pea'},
        {'name': 'lady finger', 'default_price': 45, 'default_quantity': 100, 'id': 'lady-finger'},
        {'name': 'capsicum', 'default_price': 60, 'default_quantity': 100, 'id': 'capsicum'},
        {'name': 'broccoli', 'default_price': 55, 'default_quantity': 100, 'id': 'broccoli'},
        {'name': 'cabbage', 'default_price': 30, 'default_quantity': 100, 'id': 'cabbage'},
    ],
    'freshfruit': [
        {'name': 'apple', 'default_price': 70, 'default_quantity': 100, 'id': 'apple'},
        {'name': 'banana', 'default_price': 40, 'default_quantity': 100, 'id': 'banana'},
        {'name': 'orange', 'default_price': 35, 'default_quantity': 100, 'id': 'orange'},
        {'name': 'grapes', 'default_price': 60, 'default_quantity': 100, 'id': 'grapes'},
        {'name': 'strawberry', 'default_price': 75, 'default_quantity': 100, 'id': 'strawberry'},
        {'name': 'mango', 'default_price': 80, 'default_quantity': 100, 'id': 'mango'},
        {'name': 'pineapple', 'default_price': 45, 'default_quantity': 100, 'id': 'pineapple'},
        {'name': 'watermelon', 'default_price': 55, 'default_quantity': 100, 'id': 'watermelon'},
        {'name': 'kiwi', 'default_price': 65, 'default_quantity': 100, 'id': 'kiwi'},
        {'name': 'peach', 'default_price': 50, 'default_quantity': 100, 'id': 'peach'},
    ],
    'dairybreadeggs': [
        {'name': 'milk', 'default_price': 25, 'default_quantity': 100, 'id': 'milk'},
        {'name': 'eggs', 'default_price': 12, 'default_quantity': 100, 'id': 'eggs'},
        {'name': 'butter', 'default_price': 50, 'default_quantity': 100, 'id': 'butter'},
        {'name': 'cheese', 'default_price': 55, 'default_quantity': 100, 'id': 'cheese'},
        {'name': 'yogurt', 'default_price': 30, 'default_quantity': 100, 'id': 'yogurt'},
        {'name': 'bread', 'default_price': 40, 'default_quantity': 100, 'id': 'bread'},
        {'name': 'cream', 'default_price': 60, 'default_quantity': 100, 'id': 'cream'},
        {'name': 'cottage cheese', 'default_price': 70, 'default_quantity': 100, 'id': 'cottage-cheese'},
        {'name': 'bagels', 'default_price': 45, 'default_quantity': 100, 'id': 'bagels'},
        {'name': 'cream cheese', 'default_price': 55, 'default_quantity': 100, 'id': 'cream-cheese'},
    ],
    'colddrinkjuices': [
        {'name': 'apple juice', 'default_price': 40, 'default_quantity': 100, 'id': 'apple-juice'},
        {'name': 'orange juice', 'default_price': 45, 'default_quantity': 100, 'id': 'orange-juice'},
        {'name': 'grape juice', 'default_price': 55, 'default_quantity': 100, 'id': 'grape-juice'},
        {'name': 'pineapple juice', 'default_price': 60, 'default_quantity': 100, 'id': 'pineapple-juice'},
        {'name': 'strawberry smoothie', 'default_price': 70, 'default_quantity': 100, 'id': 'strawberry-smoothie'},
        {'name': 'mango shake', 'default_price': 75, 'default_quantity': 100, 'id': 'mango-shake'},
        {'name': 'watermelon juice', 'default_price': 50, 'default_quantity': 100, 'id': 'watermelon-juice'},
        {'name': 'peach iced tea', 'default_price': 65, 'default_quantity': 100, 'id': 'peach-iced-tea'},
        {'name': 'blueberry lemonade', 'default_price': 80, 'default_quantity': 100, 'id': 'blueberry-lemonade'},
        {'name': 'cucumber mint cooler', 'default_price': 75, 'default_quantity': 100, 'id': 'cucumber-mint-cooler'},
    ],
    'teacoffeemore': [
        {'name': 'chai latte', 'default_price': 55, 'default_quantity': 100, 'id': 'chai-latte'},
        {'name': 'espresso', 'default_price': 60, 'default_quantity': 100, 'id': 'espresso'},
        {'name': 'cappuccino', 'default_price': 65, 'default_quantity': 100, 'id': 'cappuccino'},
        {'name': 'mocha', 'default_price': 70, 'default_quantity': 100, 'id': 'mocha'},
        {'name': 'green tea', 'default_price': 30, 'default_quantity': 100, 'id': 'green-tea'},
        {'name': 'iced coffee', 'default_price': 50, 'default_quantity': 100, 'id': 'iced-coffee'},
        {'name': 'Black Coffee', 'default_price': 50, 'default_quantity': 100, 'id': 'Black Coffee'},
        {'name': 'Herbal Tea', 'default_price': 50, 'default_quantity': 100, 'id': 'Herbal Tea'},
        {'name': 'Latte', 'default_price': 50, 'default_quantity': 100, 'id': 'Latte'},
        {'name': 'Turkish Coffee', 'default_price': 50, 'default_quantity': 100, 'id': 'Turkish Coffee'},]
}
selected_category = None
selected_item = None
selected_quantity = None
total_price = 0
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/category/<category_name>')
def category(category_name):
    category_options = {
        'FreshVegetable': ['Onion ', 'potato', 'Tomato', 'Cauliflower', 'Carrot', 'Pea', 'Lady finger', 'Capsicum', 'Brocoli', 'Cabbage'],
        'FreshFruit': ['Apple', 'Banana', 'Orange', 'Grapes', 'Strawberry', 'Mango', 'Pineapple', 'Watermelon', 'Kiwi', 'Peach'],
        'DairyBreadEggs':  ['Milk','Eggs','Butter','Cheese','Yogurt','Bread','Cream','Cottage Cheese','Bagels','Cream Cheese'],
        'ColdDrinkJuices':['Apple Juice', 'Orange Juice', 'Grape Juice', 'Pineapple Juice', 'Strawberry Smoothie', 'Mango Shake', 'Watermelon Juice', 'Peach Iced Tea', 'Blueberry Lemonade', 'Cucumber Mint Cooler'],
        'TeaCoffeeMore':['Chai Latte', 'Espresso', 'Cappuccino', 'Mocha', 'Green Tea', 'Iced Coffee', 'Black Coffee', 'Herbal Tea', 'Latte', 'Turkish Coffee'],
    }
    return render_template('category.html', category_name=category_name, category_options=category_options.get(category_name, []))
def item_search(user_input):
    category_options = [
        'FreshVegetable','Onion ', 'potato', 'Tomato', 'Cauliflower', 'Carrot', 'Pea', 'Lady finger', 'Capsicum', 'Brocoli', 'Cabbage',
        'FreshFruit','Apple', 'Banana', 'Orange', 'Grapes', 'Strawberry', 'Mango', 'Pineapple', 'Watermelon', 'Kiwi', 'Peach',
        'DairyBreadEggs','Milk','Eggs','Butter','Cheese','Yogurt','Bread','Cream','Cottage Cheese','Bagels','Cream Cheese',
        'ColdDrinkJuices','Apple Juice', 'Orange Juice', 'Grape Juice', 'Pineapple Juice', 'Strawberry Smoothie', 'Mango Shake', 'Watermelon Juice', 'Peach Iced Tea', 'Blueberry Lemonade', 'Cucumber Mint Cooler',
        'TeaCoffeeMore','Chai Latte', 'Espresso', 'Cappuccino', 'Mocha', 'Green Tea', 'Iced Coffee', 'Black Coffee', 'Herbal Tea', 'Latte', 'Turkish Coffee']

    items_in_category = category_options
    close_matches = get_close_matches(user_input, items_in_category, cutoff=0.1)
    return close_matches 
# Modify the /chat route to handle item search
@app.route('/chat', methods=['POST'])
def chat():
    global selected_category, selected_item, selected_quantity, total_price

    user_input = request.json.get('user_input', '').lower().strip()
    if 'hi' in user_input and selected_category is None:
        bot_response = 'Hi there! What would you like to buy? Here are some categories:\n'
        for category in category_options:
            bot_response += f'- {category}\n'
        item_search_output = item_search(user_input.lower().strip())
        return jsonify({'response': bot_response, 'item_search_output': item_search_output})
    elif selected_category is None and user_input !='proceed':
        selected_category = user_input  
        bot_response = f'Great choice! Please choose an item from {selected_category}:\n'
        for  item in category_options[selected_category]:
            bot_response += f'- {item["name"]} (Price: {item["default_price"]} INR)\n'        
    elif selected_item is None and  user_input !='proceed'  :
        selected_item = user_input
        bot_response = f'You chose {selected_item}. How many would you like to buy?'
    elif selected_quantity is None and  user_input !='proceed':
        selected_quantity = int(user_input)
        item_price = next(item['default_price'] for item in category_options[selected_category] if item['name'] == selected_item)
        total_price += item_price * selected_quantity
        bot_response = f'You have chosen {selected_quantity} {selected_item}(s) from {selected_category}. The total price is {total_price} INR. Do you want to buy more? (yes/no)'
    elif user_input == 'yes':
        selected_item, selected_quantity = None, None  
        selected_category = None
        bot_response = f'Great! Please choose another category from the categories:\n'
        for category in category_options:
            bot_response += f'- {category}\n'
    elif user_input == 'no':
        selected_category, selected_item, selected_quantity = None, None, None  
        bot_response = f'Your total bill is {total_price} INR. Would you like to proceed to payment? (yes/no)'
    elif user_input == 'proceed':
        bot_response = f'Thank you for shopping! Your payment of {total_price} INR was successful.'
        selected_category, selected_item, selected_quantity, total_price = None, None, None, 0
    else:
        # Provide item search output to the client
        item_search_output = item_search(user_input)
        return jsonify({'response': bot_response, 'item_search_output': item_search_output})
        
    return jsonify({'response': bot_response})
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1

    def search(self, prefix):
        node = self.root
        suggestions = []
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return suggestions  

        self._get_suggestions(node, prefix, suggestions)
        return suggestions

    def _get_suggestions(self, node, current_prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append((current_prefix, node.frequency))

        for char, child_node in node.children.items():
            self._get_suggestions(child_node, current_prefix + char, suggestions)
    
    def get_all_words_with_prefix(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))

        for char, child_node in node.children.items():
            self.get_all_words_with_prefix(child_node, prefix + char, suggestions)

product_data =[
        'freshvegetable','onion ', 'potato', 'tomato', 'cauliflower', 'carrot', 'pea', 'lady finger', 'capsicum', 'brocoli', 'cabbage',
        'freshFruit','apple', 'banana', 'orange', 'grapes', 'strawberry','mango', 'pineapple', 'watermelon', 'kiwi', 'peach',
        'dairyBreadEggs','milk','eggs','butter','cheese','yogurt','bread','cream','cottage Cheese','bagels','cream Cheese',
        'coldDrinkJuices','apple Juice', 'orange Juice', 'grape Juice', 'pineapple Juice', 'strawberry Smoothie', 'mango Shake', 'watermelon Juice', 'Peach Iced Tea', 'Blueberry Lemonade', 'Cucumber Mint Cooler',
        'teaCoffeeMore','chai Latte', 'espresso', 'cappuccino', 'mocha', 'green Tea', 'iced Coffee', 'black Coffee', 'herbal Tea', 'latte', 'Turkish Coffee']


trie = Trie()
for product in product_data:
    trie.insert(product)

def get_autocomplete_suggestions(prefix):
    suggestions = []
    node = trie.root
    for char in prefix.lower():
        if char in node.children:
            node = node.children[char]
        else:
            return suggestions

    trie.get_all_words_with_prefix(node, prefix.lower(), suggestions)
    sorted_suggestions = sorted(suggestions, key=lambda x: x[1], reverse=True)
    return [word for word in sorted_suggestions]
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = get_autocomplete_suggestions(prefix)
    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
