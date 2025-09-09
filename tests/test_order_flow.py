import allure
from helpers.data import Users
from pages.main_page import MainPage, HeaderPage
from pages.order_page import OrderPage


class TestOrderFlow:
    """
    Тестирование процесса оформления заказа
    """

    @allure.title('Оформление заказа через кнопку "Заказать" в хедере')
    @allure.description(
        'Проверяем заказ самоката: '
        'клик по кнопке "Заказать" в хедере, '
        'заполнение форм и подтверждение заказа.'
    )
    def test_order_scooter_from_header(self, driver):
        header_page = HeaderPage(driver)
        order_page = OrderPage(driver)
        main_page = MainPage(driver)

        main_page.accept_cookies()
        header_page.click_order_button()
        
        order_page.order_scooter_full_path(Users.user1)
        
        assert order_page.check_order_title(), "Окно с подтверждением заказа не появилось"

    @allure.title('Оформление заказа через кнопку "Заказать" на главной странице')
    @allure.description(
        'Тест оформления заказа с главной страницы: '
        'скроллим до кнопки "Заказать", кликаем, заполняем данные '
        'и подтверждаем заказ.'
    )
    def test_order_scooter_from_main_page(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        main_page.accept_cookies()
        main_page.scroll_and_click_order_button()
        
        order_page.order_scooter_full_path(Users.user2)
        
        assert order_page.check_order_title(), "Окно с подтверждением заказа отсутствует"
