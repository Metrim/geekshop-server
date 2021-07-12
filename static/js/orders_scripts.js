window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    let initial_total_forms = total_forms

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseFloat($('.order_total_cost').text()) || 0;

//Формируем массив количеств и цен:
    function updateArrayPricesQuantity() {
        total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
        quantity_arr = [];
        price_arr = [];
        console.log('total_forms ', total_forms)
        for (let i = 0; i < total_forms; i++) {
            _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]:visible').val())
            _price = parseFloat($('.orderitems-' + i + '-price:visible').text().replace(',', '.'))
            quantity_arr[i] = _quantity;
            console.log('_quantity ', _quantity)
            if (_quantity) {
                quantity_arr[i] = _quantity;
            } else {
                quantity_arr[i] = 0;
            }
            if (_price) {
                price_arr[i] = _price;
            } else {
                price_arr[i] = 0;
            }
        }
        console.log('total_forms ' + total_forms)
        console.log('quantity_arr ' + quantity_arr)
        console.log('price_arr ' + price_arr)

    }

    updateArrayPricesQuantity()

    $('.order_form').on('click', 'input[type=number]', function () {
        // Below example worked with orderSummaryUpdate(orderitem_price, delta_quantity):
        // let target = event.target; //  Выбираем на какой объект щелкнул пользователь
        // orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', '')); // выбираем на какой строке пользователь
        // if (price_arr[orderitem_num]) {
        //     orderitem_quantity = parseInt(target.value);
        //     delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
        //     quantity_arr[orderitem_num] = orderitem_quantity
        // }

        orderSummaryRecalc();
    });


    $('.order_form').on('click', 'input[type=checkbox]', function () {
        // Below example worked with orderSummaryUpdate(orderitem_price, delta_quantity):
        // let target = event.target; //  Выбираем на какой объект щелкнул пользователь
        // orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        // if (target.checked) {
        //     delta_quantity = -quantity_arr[orderitem_num];
        // } else {
        //     delta_quantity = quantity_arr[orderitem_num];
        // }

        orderSummaryRecalc();
    });


    // Changed this function implementation to the orderSummaryRecalc(); This entry only for history as example from lesson:
    // function orderSummaryUpdate(orderitem_price, delta_quantity) {
    //     delta_cost = orderitem_price * delta_quantity;
    //     console.log('delta_cost '+delta_cost)
    //     order_total_price = Number((order_total_price + delta_cost).toFixed(2));
    //     console.log('order_total_price '+order_total_price)
    //     order_total_quantity = order_total_quantity + delta_quantity;
    //     console.log('order_total_quantity '+order_total_quantity)
    //
    //
    //     $('.order_total_quantity').text(order_total_quantity.toString());
    //     $('.order_total_cost').text(order_total_price.toString());
    // }
    //

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
        added: addOrderItem,
    });

    function deleteOrderItem(row) {
        orderSummaryRecalc();
        // Changed this function implementation to the orderSummaryRecalc(); This entry only for history as example from lesson:
        // let target_name = row[0].querySelector('input[type=number]').name;
        // orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        // delta_quantity = -quantity_arr[orderitem_num];
        // orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
        // updateArrayPricesQuantity()
    }

    function addOrderItem() {
        updateArrayPricesQuantity();
        let current_tr = $('.order_form table').find('tr:eq(' + total_forms + ')');
        current_tr.find('input[type="number"]').val(0);
        updateSelectChangeHandler();
    }

    // Window onload call of the function:
    updateSelectChangeHandler()

    function updateSelectChangeHandler() {
        $('.order_form select').change(function () {
            let target = event.target;
            orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
            console.log('orderitem_num', orderitem_num)
            let order_item_product_pk = target.options[target.selectedIndex].value;
            console.log('order_item_product_pk ' + order_item_product_pk)
            if (order_item_product_pk === '') {
                order_item_product_pk = 0
                console.log('order_item_product_pk ' + order_item_product_pk)
            }

            if (order_item_product_pk || order_item_product_pk === 0) {
                $.ajax({
                    url: '/order/product/' + order_item_product_pk + '/price/',
                    success: function (data) {
                        if (data.price || data.price === 0) {
                            console.log('success data.price', data.price)
                            price_arr[orderitem_num] = parseFloat(data.price);
                            if (isNaN(quantity_arr[orderitem_num])) {
                                quantity_arr[orderitem_num] = 0;
                            }
                            let price_html ='<span class="orderitems-' + orderitem_num + '-price">' + data.price.toString().replace(".", ",") + '&nbsp;руб</span>'
                            let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                            current_tr.find('td:eq(2)').html(price_html);
                            if (data.price === 0) {
                                current_tr.find('input[type="number"]').val(0);
                            }
                            orderSummaryRecalc();
                        }
                    }
                });
            }
        });
    }

    function orderSummaryRecalc() {
        order_total_quantity = 0;
        order_total_price = 0;
        console.log('ordersummaryrecalc')
        updateArrayPricesQuantity()
        for (let i = 0; i < total_forms; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_price += quantity_arr[i] * price_arr[i];
        }

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toFixed(2).toString());

    }

};