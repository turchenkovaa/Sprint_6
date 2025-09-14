from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException


class BasePage:
    """
    Общий базовый класс для страниц с вспомогательными методами
    """
    
    def __init__(self, driver):
        self.driver = driver

    def wait_until_visible(self, locator, timeout=10):
        """Подождать, пока элемент станет видимым"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_present(self, locator, timeout=10):
        """Ждать появления элемента в DOM"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_current_url(self):
        """Получение текущего URL страницы"""
        return self.driver.current_url

    def find_and_wait_locator(self, locator):
        """Поиск и ожидание элемента"""
        return self.wait_until_visible(locator, timeout=10)

    def click_button(self, locator, retries=3, delay=0.5):
        """Нажатие по элементу с fallback на JavaScript и обработкой stale элементов"""
        for _ in range(retries):
            try:
                element = self.find_and_wait_locator(locator)
                element.click()
                return
            except (ElementClickInterceptedException, ElementNotInteractableException):
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except StaleElementReferenceException:
                    pass  # Элемент устарел — retry
            except StaleElementReferenceException:
                pass  # Элемент устарел — retry
            time.sleep(delay)
        raise Exception(f"Не удалось кликнуть по элементу с локатором {locator}")

    def send_keys_to_field(self, locator, text):
        """Очистить поле и ввести текст"""
        element = self.find_and_wait_locator(locator)
        element.clear()
        element.send_keys(text)

    def get_text_locator(self, locator):
        """Получить текст элемента"""
        return self.find_and_wait_locator(locator).text

    def scroll_to_locator(self, locator):
        """Скролл к элементу с центрированием"""
        element = self.find_and_wait_locator(locator)
        # Скролл с отступом, чтобы элемент был виден и не перекрывался
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        # Доп скролл вверх, чтобы избежать перекрытия изображением
        self.driver.execute_script("window.scrollBy(0, -100);")
        # Ожидаем завершения анимации скролла
        WebDriverWait(self.driver, 2).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def go_to_new_tab(self):
        """Ожидать появления новой вкладки"""
        # Открываем новую вкладку
        self.driver.execute_script("window.open('');")
        # Обновляем список окон
        window_handles = self.driver.window_handles
        # Переключаемся на последнюю вкладку
        self.driver.switch_to.window(window_handles[-1])
    

    def check_element(self, locator):
        """Проверка отображения элемента"""
        return self.find_and_wait_locator(locator).is_displayed()

    def wait_for_page_ready(self, timeout=5):
        """Ожидание готовности страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element_clickable(self, locator, timeout=5):
        """Ожидание кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def execute_js_script(self, script):
        """Выполнение JavaScript скрипта"""
        return self.driver.execute_script(script)

    def blur_element(self, element):
        """Убрать фокус с переданного элемента через JS"""
        self.execute_js_script("arguments[0].blur();", element)

    def hide_element_by_class(self, class_name):
        """Скрыть элемент по классу"""
        script = f"""
            var element = document.querySelector('.{class_name}');
            if (element) {{
                element.style.display = 'none';
            }}
        """
        self.execute_js_script(script)

    def click_element_by_class(self, class_name):
        """Нажать по элементу по классу"""
        script = f'document.querySelector(".{class_name}").click();'
        self.execute_js_script(script)

    def click_element_by_xpath(self, xpath):
        """Нажать по элементу по XPath"""
        element = self.driver.find_element("xpath", xpath)
        element.click()

    def wait_for_new_window(self, initial_windows_count, timeout=10):
        """Ждать открытия новой вкладки"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > initial_windows_count
        )

    def wait_for_page_title_loaded(self, timeout=10):
        """Ждать загрузки заголовка страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.title and len(d.title.strip()) > 0
        )

    def get_page_title(self):
        """Получить заголовок страницы"""
        return self.driver.title

    def get_windows_count(self):
        """Получить количество открытых окон"""
        return len(self.driver.window_handles)

    def wait_for_url_change_from_about_blank(self, timeout=10):
        """Ждать изменения URL с about:blank"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url != "about:blank" and "about:" not in d.current_url
        )
