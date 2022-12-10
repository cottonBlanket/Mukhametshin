Результаты профилирования Парсера дат
Для проведения тестирования парсинга дат публикации вакансии написал класс DateTimeParser содержащий 4 метода:
Каждый метод по-разному вычленяет из строки год публикации

1. С помощью класса datetime

  ![image](https://user-images.githubusercontent.com/102159807/206877359-988f4c80-b4dc-4de8-af05-161efdd6565f.png)
  
  Результат профилирования 
  ![image](https://user-images.githubusercontent.com/102159807/206877390-c71f2389-284b-4516-a17e-92a11318d9c5.png)

2. С помощью метода split
  
  ![image](https://user-images.githubusercontent.com/102159807/206877407-f9823a88-1645-4e2e-bed6-34c0e5fc6a0e.png)

  Результат профилирования 
  ![image](https://user-images.githubusercontent.com/102159807/206877431-7782dd7f-3466-4a29-8cfc-60ad10ef16e5.png)

3. С помощью индексирования строк
  
  ![image](https://user-images.githubusercontent.com/102159807/206877443-b3f6bdae-f7a9-4ae4-bd28-8b7020bd2ea4.png)

  Результат профилирования
  ![image](https://user-images.githubusercontent.com/102159807/206877467-dee59105-727f-49d7-bd47-5c90a46271ea.png)

4. С помощью класса dateparser

  ![image](https://user-images.githubusercontent.com/102159807/206877483-a14e6dcf-f7dc-449a-88b2-912caa80e8ec.png)

  Результат профилирования
  ![image](https://user-images.githubusercontent.com/102159807/206877733-1a01f1a1-acbe-4a4d-8803-e0a52731af57.png)
