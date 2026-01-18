document.addEventListener('DOMContentLoaded', () => {

    // استرجاع السلة من localStorage أو إنشاء مصفوفة جديدة
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');

    // عناصر الـ DOM
    const cartItemsContainer = document.querySelector('.cart-items');
    const cartTotal = document.getElementById('cart-total');
    const cartCount = document.getElementById('cart-count'); // ← هنا يظهر الإجمالي
    const checkoutBtn = document.getElementById('checkout-btn');

    // تحديث زر checkout
    function updateCheckoutButton() {
        if(!checkoutBtn) return;
        if(cart.length === 0){
            checkoutBtn.disabled = true;
            checkoutBtn.classList.add('opacity-50');
        } else {
            checkoutBtn.disabled = false;
            checkoutBtn.classList.remove('opacity-50');
        }
    }

    // تحديث محتوى السلة
    function updateCart(){
        if(cartItemsContainer) cartItemsContainer.innerHTML = '';

        let totalPrice = 0;
        let totalCount = 0;

        cart.forEach(item => {
            totalPrice += item.price * item.quantity;
            totalCount += item.quantity;

            if(cartItemsContainer){
                const div = document.createElement('div');
                div.className = 'cart-item d-flex align-items-start mb-3 p-2 border rounded';
                div.innerHTML = `
                    <img src="${item.img}" class="cart-item-img rounded me-2" style="width:60px; height:60px; object-fit:cover;">
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center">
                            <p class="mb-1 fw-medium">${item.name}</p>
                            <button type="button" class="btn-close remove-item" data-id="${item.id}"></button>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mt-2">
                            <div class="item-quantity d-flex align-items-center">
                                <button class="btn btn-sm decrease" data-id="${item.id}">-</button>
                                <input type="number" value="${item.quantity}" class="form-control form-control-sm mx-1" style="width:50px;" data-id="${item.id}">
                                <button class="btn btn-sm increase" data-id="${item.id}">+</button>
                            </div>
                            <p class="mb-0 fw-bold">${item.price * item.quantity} جنيه</p>
                        </div>
                    </div>
                `;
                cartItemsContainer.appendChild(div);
            }
        });

        if(cartTotal) cartTotal.textContent = totalPrice + ' جنيه';
        if(cartCount) cartCount.textContent = totalPrice; // ← تحديث cart-count هنا

        // حفظ السلة في localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCheckoutButton();
    }

    // إضافة عنصر للسلة
    document.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', e => {
            const parent = e.target.closest('.product-item');
            const id = parent.dataset.id;
            const name = parent.dataset.name;
            const price = parseInt(parent.dataset.price);
            const img = parent.dataset.img;
            const amountInput = parent.querySelector('input[name="amount"]');
            let quantity = parseInt(amountInput.value) || 1;

            if(quantity <= 0){
                alert('الرجاء إدخال كمية أكبر من 0');
                return;
            }

            const existing = cart.find(i => i.id === id);
            if(existing){
                existing.quantity += quantity;
            } else {
                cart.push({id,name,price,img,quantity});
            }

            updateCart();

            // فتح مودال السلة
            const cartModalEl = document.getElementById('cartModal');
            const modal = bootstrap.Modal.getOrCreateInstance(cartModalEl);
            modal.show();
        });
    });

    // أحداث تعديل/حذف
    if(cartItemsContainer){
        cartItemsContainer.addEventListener('click', e => {
            const id = e.target.dataset.id;
            const item = cart.find(i => i.id===id);
            if(!item) return;

            if(e.target.classList.contains('remove-item')){
                cart = cart.filter(i=>i.id!==id);
            }
            if(e.target.classList.contains('increase')) item.quantity++;
            if(e.target.classList.contains('decrease')) item.quantity = Math.max(1, item.quantity-1);

            updateCart();
        });

        cartItemsContainer.addEventListener('input', e => {
            if(e.target.tagName==='INPUT'){
                const id = e.target.dataset.id;
                const item = cart.find(i=>i.id===id);
                if(item) item.quantity = Math.max(1, parseInt(e.target.value)||1);
                updateCart();
            }
        });
    }

    // مسح الكل
    const clearBtn = document.getElementById('clear-cart');
    if(clearBtn){
        clearBtn.addEventListener('click', ()=>{
            cart=[];
            updateCart();

            const cartModalEl = document.getElementById('cartModal');
            const modal = bootstrap.Modal.getInstance(cartModalEl);
            if(modal) modal.hide();
        });
    }

    // تحميل السلة عند فتح الصفحة
    updateCart();
});
