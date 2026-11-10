def print_select_menu() :
    print("\n"+"-"*40)
    print("1.상품목록 2.담기 3.빼기 4.장바구니 5.쿠폰 6.결제 q.종료")
    print("-"*40)

class Product : #(번호, 상품명, 가격, 재고)
    def __init__(self, product_id, name, price, inventory) :
        self.product_id = product_id
        self.name = name
        self.price = price
        self.inventory = inventory


class Discount :
    def __init__(self, rate = 0, amount = 0): # 할인율, 할인액 기본값 0으로 설정. 한도 없으면 Discount 클래스 사용
        self.name = "쿠폰 없음"
        self.rate = rate
        self.amount = amount

    def discount(self, total): 
        result = total * self.rate + self.amount # % 먼저 계산하고 정액 차감한다고 가정 
        return result


class RateDiscount(Discount):
    def __init__ (self, rate, max_amount) :

        super().__init__()

        self.name = f"{rate*100}% 쿠폰 (한도 {max_amount}원)"
        self.rate = rate
        self.max_amount = max_amount

    def discount(self, total) :
        if total * self.rate > self.max_amount :
            return self.max_amount #할인 최대금액은 5,000원을 넘을 수 없음
        result = total * self.rate
        return result

class FixedDiscount(Discount):
    def __init__ (self, amount, min_total) :

        super().__init__()

        self.name = f"{amount}원 쿠폰 (최소사용금액 {min_total}원)"
        self.amount = amount
        self.min_total = min_total

    def discount(self, total) :

        if total >= self.min_total : return self.amount

        else : return 0
    
     



# 이름, 가격, 재고를 리스트에 적어놓고 이를 바탕으로 객체 생성
def make_product_list(name_list, price_list, inventory_list) :
    product_list = [] 
    for i in range(0, len(name_list)) :
        product = Product(i+1, name_list[i], price_list[i], inventory_list[i])
        product_list.append(product)

    return product_list #객체들을 모아놓은 리스트가 결과로 나옴
    #[객체1, 객체2, 객체3 ...] 리스트 인덱스가 기본키 역할을 하게됨



def print_all_products(product_list) :
    #Product 객체들을 담은 리스트에서 하나씩 꺼내 프린트
    for pd in product_list :
        print(f"{pd.product_id}. {pd.name:<10}{pd.price:>5,} (재고 {pd.inventory}개)")


# 장바구니는 딕셔너리 형태 {제품번호 -1 : 담은 수량 ... }
def add_cart_qty (cart_qty, product_list) :

    user_num = int(input("상품 번호 : "))
    pd_idx = user_num - 1 # 2번 제품은 product_list[1]

    if pd_idx >= len(product_list) :  # 상품 목록에 없는 제품을 불러옴
        print("\n목록에 없는 상품입니다.")
        return cart_qty 
    
    if product_list[pd_idx].inventory == 0 : # 품절
        print("\n품절된 상품입니다.")
        return cart_qty
    
    user_qty = int(input("수량 : "))
    if product_list[pd_idx].inventory < user_qty : # 재고부족
        print(f"\n재고가 부족합니다. (담을 수 있는 수량 : {product_list[pd_idx].inventory}개)")
        return cart_qty

    # 장바구니에 유저가 고른 제품과 같은 제품이 들어있는지 조회
    if pd_idx in cart_qty :
        if product_list[pd_idx].inventory - cart_qty[pd_idx] < user_qty : # 재고 - 장바구니에 담은 수량 < 추가수량  불가능함     
            print(f"\n재고가 부족합니다. (담을 수 있는 수량 : {product_list[pd_idx].inventory-cart_qty[pd_idx]}개)")
            return
        cart_qty[pd_idx] += user_qty
    else : 
        cart_qty[pd_idx] = user_qty

    return cart_qty

def sub_cart_qty (cart_qty, product_list) :

    # 장바구니가 비었으면 빼기기능 실행하지 않고 종료
    if cart_qty == {} :
        print("\n장바구니 내역이 없습니다.")
        return cart_qty

    user_num = int(input("상품 번호 : "))
    pd_idx = user_num - 1

    if not pd_idx in cart_qty :
        print("\n장바구니에 담아 놓은 제품을 골라주세요.")
        return cart_qty

    user_qty = int(input("수량 : "))  
    if cart_qty[pd_idx] < user_qty : # 장바구니 수량보다 더 많이 빼려고하는 상황
        print("\n장바구니에 담긴 수량보다 더 많은 수량을 빼려고 합니다.(남은 수량 전부 차감)")
        cart_qty[pd_idx] = 0 # 그냥 수량 0으로 맞춤
    else :
        cart_qty[pd_idx] -= user_qty

    return cart_qty


def show_cart_total (cart_qty, product_list) :

    if cart_qty == {} :  
        print("\n"+"-"*40)
        print("\n장바구니 내역이 없습니다.")
        print("-"*40)
        return

    total = 0
    print("-"*40)
    for pd_idx, qty in sorted(cart_qty.items()) : 
        print(f"{product_list[pd_idx].name:<10} x {qty:<5} {product_list[pd_idx].price * qty:>15,}원")
        total += product_list[pd_idx].price * qty
    print("-"*40)
    print(f"상품 합계 {total:>30,}")
    print(f"할인{coupon_list[picked_coupon_idx].discount(total):>30,}")
    print(f"결제 금액 {total - coupon_list[picked_coupon_idx].discount(total):>30,}")


def choose_menu() :
    menu_list = ["1","2","3","4","5","6","q"]
    while True :
        print_select_menu() # 선택 목록 출력 
        user_choose = input("선택 : ").lower().strip()
        print("\n")
        if user_choose in menu_list :
            break
        print("선택 목록에 있는 기능을 고르세요.")

    return user_choose

def show_coupon_list(coupon_list) :
    for cp in coupon_list :
        print(cp.name)
    picked_coupon_idx = int(input("쿠폰 번호 : ")) - 1
    return picked_coupon_idx


def get_pay (cart_qty, product_list) :

    if cart_qty == {} : # 장바구니가 비었기 때문에 결제할 금액이 없음
        print("장바구니가 비었습니다.") 
        return (cart_qty, product_list)

    for pd_idx, qty in sorted(cart_qty.items()) :
        product_list[pd_idx].inventory -= qty # 장바구니 수량만큼 재고 감소


        del cart_qty[pd_idx] # 재고 감소시킨 장바구니 품목 장바구니에서 제거

    print("(영수증 출력)")
    print("결제가 완료되었습니다. 감사합니다!\n")
    return (cart_qty, product_list)
    



# 데이터관리는 product_list로 진행함, 처음 클래스 생성용으로 리스트 만들었음
name_list = ["무선 이어폰", "텀블러", "보조배터리", "마우스패드", "USB 허브"]
price_list = [89000, 15000, 32000, 9000, 18000]
inventory_list = [3, 10, 5, 0, 4]
# 위 3개 리스트를 가지고 product_list를 만듬 [product객체1, product객체2 ....]
product_list = make_product_list(name_list, price_list, inventory_list)

coupon_list = [Discount(),
               RateDiscount(0.1, 5000),
               FixedDiscount(3000, 20000)]

cart_qty = {}    # 장바구니 {pd_idx : qty, ...}   
# 현재는 수량만 장바구니로 관리하는데, 나중에 기능을 추가하려면 딕셔너리를 새로 만들어야할 것 같다.




# 메인 구조
while True :
    user_choose = choose_menu()

    if user_choose == "1":
        print_all_products(product_list)
    if user_choose == "2":
        cart_qty = add_cart_qty(cart_qty, product_list)
    if user_choose == "3":
        cart_qty = sub_cart_qty(cart_qty, product_list)
    if user_choose == "4":
        show_cart_total(cart_qty, product_list)
    if user_choose == "5":
        picked_coupon_idx = show_coupon_list(coupon_list)
    if user_choose == "6":
        cart_qty, product_list = get_pay(cart_qty, product_list)
    if user_choose == "q" :    # 유저가 q 입력하면 그만둠
        break







