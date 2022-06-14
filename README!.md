## SOAP LOAD TEST
В данном нагрузочном тесте используются SOAP запросы:  
* NewRx
* RxHistory  
* RxPharmacyHistory  
* RxCancel  
* PharmacyCancelRx  
* RxPharmacyHistory  
* RxFill  
* RxDelayedFill  
  
Запросы собраны в логических контроллерах - Script1, Script2, Script3, Script4.
* Script1  
  * RxHistory  
  * RxPharmacyHistory  
  * RxCancel  
* Script2  
  * RxPharmacyHistory  
  * PharmacyCancelRx  
* Script3  
  * RxPharmacyHistory  
  * RxFill  
* Script4
  * RxPharmacyHistory  
  * RxDelayedFill  
  
Логические контроллеры хранятся в **bzm - Weighted Switch Controller**, из которого рандомно вызываются.  

# Конфигурация и запуск
  
Для запуска теста нужно сконфигурировать значения полей:  
1. **Number of Threads**   
2. **Ramp-up period**   
3. **Loop Count**   
4. **Same user on each iteration**
  
Указать данные значения можно запустив **jmeter** и перейдя в раздел **Thread Group**.
Запуск **jmeter**

    $ cd ../apache-jmeter-5.4.3/bin
    $ ./jmeter 
    
  Также перед запуском  нужно сконфигурировать стенд [Dev, Pre-Prod или Prod]
  
 Чтобы изменить стенд,  нужно перейти в **HTTP Request Defaults** и в поле **Server Name or IP** указать нужный URL, например **api.medicata.dev**
    

## Запуск теста
Запускать тесты нужно из директории `cd ../apache-jmeter-5.4.3/bin`
**Команда для запуска**

    ./jmeter.sh -n -t /home/{Папка с тестом}/{Нагрузочный тест}.jmx -l /home/{Папка с тестом}/Result/{Имя для файла с отчётом}.csv -e -o /home/{Папка с тестом}/HtmlReport
