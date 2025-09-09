import allure
from pages.main_page import HeaderPage, MainPage
from pages.order_page import OrderPage
from helpers.data import Users


class TestLogos:
    """
    Тесты для проверки работы логотипов
    """

    @allure.title('Редирект по логотипу Самоката с главной страницы')
    @allure.description('Убедиться, что клик по логотипу Самоката не меняет URL')
    def test_scooter_logo_redirect_from_main_page(self, driver):
        header_page = HeaderPage(driver)
        main_page = MainPage(driver)
        
        main_page.accept_cookies()
        initial_url = main_page.get_current_url()
        
        header_page.click_scooter_logo()
        
        # Проверка URL (он не изменился, то есть остались на главной странице)
        current_url = main_page.get_current_url()
        assert current_url == initial_url, f"URL изменился после того, как нажали на лого Самоката: {current_url}"

    @allure.title('Редирект при клике на логотип Яндекса')
    @allure.description('Проверяем открытие новой вкладки с Дзеном после клика по логотипу Яндекса')
    def test_yandex_logo_redirect(self, driver):
        header_page = HeaderPage(driver)
        main_page = MainPage(driver)
        

        main_page.accept_cookies()
        initial_windows_count = main_page.get_windows_count()
        
        # Клик по логу Яндекса
        header_page.click_yandex_logo()
        
        # Открывается новая вкладка
        main_page.wait_for_new_window(initial_windows_count)
        
        # Проверка открытия новой вкладки
        new_windows_count = main_page.get_windows_count()
        assert new_windows_count > initial_windows_count, "Новая вкладка не открылась"
        
        # Переключаемся на новую вкладку
        header_page.go_to_new_tab()
        
        # Ожидаем загрузку страницы в новой вкладке
        main_page.wait_for_page_ready(10)
        
        # Ожидаем пока URL изменится с about:blank
        main_page.wait_for_url_change_from_about_blank(10)
        
        # Проверка URL новой вкладки
        current_url = main_page.get_current_url()
        assert "dzen.ru" in current_url or "yandex.ru" in current_url, \
            f"Новая вкладка не содержит ожидаемый URL: {current_url}"
        
        # Проверяем заголовок страницы и ожидаем загрузки заголовка страницы
        main_page.wait_for_page_title_loaded()
        page_title = main_page.get_page_title()
        assert "Дзен" in page_title or "Яндекс" in page_title or "Yandex" in page_title, \
            f"Заголовок страницы не соответствует ожиданиям: {page_title}"

    @allure.title('Редирект со страницы заказа по логотипу Самоката')
    @allure.description('Кликаем по логотипу Самоката с страницы заказа и возвращаемся на главную')
    def test_scooter_logo_redirect_from_order_page(self, driver):
        header_page = HeaderPage(driver)
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        main_page.accept_cookies()
        
    
        main_page.scroll_and_click_order_button()
        order_page.complete_filling_of_the_who_is_scooter_form(Users.user1)
        
        header_page.click_scooter_logo()
        
        # Проверяем, что вернулись на главную страницу
        current_url = main_page.get_current_url()
        assert "order" not in current_url, f"Остались на странице заказа: {current_url}"

    @allure.title('Проверка атрибутов логотипов')
    @allure.description('Проверяем ссылки и атрибуты логотипов Самоката и Яндекса')
    def test_logos_attributes(self, driver):
        header_page = HeaderPage(driver)
        main_page = MainPage(driver)
        
        # Принимаем cookies
        main_page.accept_cookies()
        
        # Проверяем, что логотипы являются ссылками
        assert header_page.is_logo_link('scooter'), "Логотип Самоката не является ссылкой"
        assert header_page.is_logo_link('yandex'), "Логотип Яндекса не является ссылкой"
        
        # Проверяем target="_blank" для логотипа Яндекса
        yandex_target = header_page.get_logo_target('yandex')
        assert yandex_target == '_blank', f"Логотип Яндекса не имеет target='_blank': {yandex_target}"
        
        # Проверяем href атрибуты
        scooter_href = header_page.get_logo_href('scooter')
        yandex_href = header_page.get_logo_href('yandex')
        
        assert scooter_href is not None, "Логотип Самоката не имеет href атрибута"
        assert yandex_href is not None, "Логотип Яндекса не имеет href атрибута"
