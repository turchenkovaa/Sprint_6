import allure
import pytest
from helpers.data import FAQAnswers
from pages.main_page import MainPage


class TestFAQ:
    """
    Проверка функциональности раздела FAQ
    """

    @allure.title('Проверка общего количества вопросов FAQ')
    @allure.description('Удостоверяемся, что на странице отображаются ровно 8 вопросов в разделе FAQ')
    def test_faq_questions_count(self, driver):
        main_page = MainPage(driver)
        main_page.accept_cookies()
        questions_count = main_page.get_faq_questions_count()
        assert questions_count == 8, f"Ожидалось 8 вопросов, но получено {questions_count}"

    @allure.title('Проверка отображения раздела FAQ')
    @allure.description('Подтверждаем, что раздел "Вопросы о важном" виден на странице')
    def test_faq_section_visible(self, driver):
        main_page = MainPage(driver)
        main_page.accept_cookies()
        assert main_page.is_faq_section_visible(), "Раздел FAQ не найден или скрыт"

    @pytest.mark.parametrize("question_index,expected_answer", 
                            [(i, FAQAnswers.expected_answers[i]) for i in range(8)],
                            ids=[f"question_{i}" for i in range(8)])
    @allure.title('Проверка правильных ответов на вопросы FAQ')
    @allure.description('аждое нажатие на вопрос должно показывать соответствующий ответ')
    def test_faq_answers(self, driver, question_index, expected_answer):
        """
        Тест клика по вопросам FAQ и проверки отображаемых ответов
        """
        main_page = MainPage(driver)
        main_page.accept_cookies()
        
        actual_answer = main_page.get_faq_answer_text(question_index)
        
        assert actual_answer == expected_answer, \
            f"Ожидался ответ: '{expected_answer}', получен: '{actual_answer}'"
