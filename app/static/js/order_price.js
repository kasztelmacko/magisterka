let order_price = 0;
const orderedItems = [];

function addToCart(itemName, price) {
    order_price += price;
    orderedItems.push({ name: itemName, price: price });
    updateOrderButton();
    updateCartItems();
}

function removeFromCart(itemName, price) {
    // Find and remove item from orderedItems array
    const index = orderedItems.findIndex(item => item.name === itemName && item.price === price);
    if (index !== -1) {
        orderedItems.splice(index, 1);
        order_price -= price;
        updateOrderButton();
        updateCartItems();
    }
}

function cancelOrder() {
    // Cancel functionality can be added here
}

function updateOrderButton() {
    const orderButton = document.getElementById('order-button');
    if (order_price > 0) {
        orderButton.innerText = `Order (${order_price} zł)`;
        orderButton.classList.remove('bg-gray-400', 'cursor-not-allowed');
        orderButton.classList.add('bg-success', 'hover:bg-btn-accept-hover', 'cursor-pointer');
        orderButton.disabled = false;
    } else {
        orderButton.innerText = 'Order';
        orderButton.classList.remove('bg-success', 'hover:bg-btn-accept-hover', 'cursor-pointer');
        orderButton.classList.add('bg-gray-400', 'cursor-not-allowed');
        orderButton.disabled = true;
    }
}

function updateCartItems() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = ''; // Clear existing items

    orderedItems.forEach((item, index) => {
        // Create hidden input for each item
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = `items[${index}]`; // Using index to ensure unique names
        input.value = JSON.stringify(item);
        cartItemsDiv.appendChild(input);

        // Create visible div for each item (if you still want to display the items in the cart)
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('flex', 'items-center', 'justify-between', 'w-full', 'text-lg', 'font-bold', 'text-gray-900', 'dark:text-white', 'mb-1');
        itemDiv.innerHTML = `
            <div class="flex items-center gap-x-1">
                <span>${item.name} ${item.price} zł</span>
                <button class="ml-2 text-red-500 hover:text-red-700" type="button" onclick="removeFromCart('${item.name}', ${item.price})">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="red">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    <span class="inline-block ml-1 text-xs text-red-500"></span>
                </button>
            </div>
        `;
        cartItemsDiv.appendChild(itemDiv);
    
    });

    // Update the order button state based on the items present
    updateOrderButtonState();
}

function collectOrderJson(orderedItems) {
    let orderJson = { ordered_items: {} };

    orderedItems.forEach(item => {
        orderJson.ordered_items[item.name] = {
            item_price: item.price,
            price_type: item.price_type
        };
    });

    return orderJson;
}
