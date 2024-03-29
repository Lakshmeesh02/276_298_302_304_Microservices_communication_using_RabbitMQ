from flask import Flask, request, jsonify

app=Flask(__name__)

inventory=[]

@app.route('/')
def home():
    return "Hello world"

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/inventory', methods=['POST'])
def create_item():
    data=request.get_json()
    inventory.append(data)
    return jsonify({'message: Item created successfully'}), 201

@app.route('/inventory', methods=['GET'])
def get_items():
    return jsonify(inventory)

@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data=request.get_json()
    if item_id<len(inventory):
        inventory[item_id]=data
        return jsonify({'message: Item updated successfully'})
    else:
        return jsonify({'error: Item not found'}), 404
    
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id<len(inventory):
        inventory.pop(item_id)
        return jsonify({'message: Item deleted successfully'})
    else:
        return jsonify({'error: Item not found'}), 404
    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)