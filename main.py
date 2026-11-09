def print_select_menu() :
    print("-"*40)
    print("1.상품목록 2.담기 3.빼기 4.장바구니 5.쿠폰 6.결제 q.종료")
    print("-"*40)

class Product : #(번호, 상품명, 가격, 재고)
    def __init__(self, product_id, name, price, inventory) :
        self.product_id = product_id
        self.name = name
        self.price = price
        self.inventory = inventory



# 이름, 가격, 재고를 리스트에 적어놓고 이를 바탕으로 객체 생성
def make_product_list(name_list, price_list, inventory_list) :
    product_list = [] 
    for i in range(0, len(name_list)) :
        product = Product(i+1, name_list[i], price_list[i], inventory_list[i])
        product_list.append(product)

    return product_list #객체들을 모아놓은 리스트가 결과로 나옴


def print_all_products(product_list) :
    #Product 객체들을 담은 리스트에서 하나씩 꺼내 프린트
    for pd in product_list :
        print(f"{pd.product_id}. {pd.name:<10}{pd.price:>5,} (재고 {pd.inventory}개)")


# 장바구니는 딕셔너리 형태 {제품번호 -1 : 담은 수량 ... }
def add_cart_item (cart_qty, product_list) :
    # 담기 전에 장바구니 내역 보여줌
    if cart_qty == {} : # 빈 장바구니
        print("장바구니 내역이 없습니다.")
    else :
        print("---------------장바구니 내역---------------")
        for pd_idx, qty in sorted(cart_qty.items()) :  # pd_idx 정렬하고 idx, 수량 차례로 뽑음
            print(f"{pd_idx+1}. {product_list[pd_idx].name} : {qty}개")        
            print("-"*40)

    user_num = int(input("상품 번호 : "))
    pd_idx = user_num - 1 # 2번 제품은 product_list[1]

    if product_list[pd_idx].inventory == 0 : # 품절
        print("품절된 상품입니다.")
        return cart_qty
    
    user_qty = int(input("수량 : "))
    if product_list[pd_idx].inventory < user_qty : # 재고부족
        print(f"재고가 부족합니다. (담을 수 있는 수량 : {product_list[pd_idx].inventory}개)")
        return cart_qty

    # 장바구니에 유저가 고른 제품과 같은 제품이 들어있는지 조회
    if pd_idx in cart_qty :
        if product_list[pd_idx].inventory - cart_qty[pd_idx] < user_qty : # 재고 - 장바구니에 담은 수량 < 추가수량  불가능함     
            print(f"재고가 부족합니다. (담을 수 있는 수량 : {product_list[pd_idx].inventory-cart_qty[pd_idx]}개)")
            return
        cart_qty[pd_idx] += user_qty
    else : 
        cart_qty[pd_idx] = user_qty

    return cart_qty

def sub_cart_item (cart_qty, product_list) :
    # 장바구니가 비었으면 빼기기능 실행하지 않고 종료
    if cart_qty == {} :
        print("장바구니 내역이 없습니다.")
        return cart_qty
    # 빼기전에 장바구니 내역을 보여줌
    print("---------------장바구니 내역---------------")
    for pd_idx, qty in sorted(cart_qty.items()) :  # pd_idx 정렬하고 idx, 수량 차례로 뽑음
        print(f"{pd_idx+1}. {product_list[pd_idx].name} : {qty}개")        
    print("-"*40)

    user_num = int(input("상품 번호 : "))
    pd_idx = user_num - 1

    if not pd_idx in cart_qty :
        print("장바구니에 담아 놓은 제품을 골라주세요.")
        return cart_qty

    user_qty = int(input("수량 : "))  
    if cart_qty[pd_idx] < user_qty : # 장바구니 수량보다 더 많이 빼려고하는 상황
        print("장바구니에 담긴 수량보다 더 많은 수량을 빼려고 합니다.")
        cart_qty[pd_idx] = 0 # 그냥 수량 0으로 맞춤
    else :
        cart_qty[pd_idx] -= user_qty

    return cart_qty


    
    



# 데이터관리는 product_list로 진행함, 처음 클래스 생성용으로 리스트 만들었음
name_list = ["무선 이어폰", "텀블러", "보조배터리", "마우스패드", "USB 허브"]
price_list = [89000, 15000, 32000, 9000, 18000]
inventory_list = [3, 10, 5, 0, 4]
cart_qty = {}    # 장바구니 {pd_idx : qty ...}


print_select_menu()
product_list = make_product_list(name_list, price_list, inventory_list)
print_all_products(product_list) # 1. 상품목록
cart_qty = add_cart_item(cart_qty, product_list)
cart_qty = add_cart_item(cart_qty, product_list)
cart_qty = sub_cart_item(cart_qty, product_list)
cart_qty = sub_cart_item(cart_qty, product_list)





