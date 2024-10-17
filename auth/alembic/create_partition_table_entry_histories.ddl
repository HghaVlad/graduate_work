/*
АВТОР: Тараканов Денис
СОЗДАНО: 18.08.2024
E-MAIL: deniskatarakanov@yandex.ru
ОПИСАНИЕ: Данный DDL-файл содержит перечень SQL-запросов,
необходимых для создания партицированных таблиц:
	- entry_histories_console
	- entry_histories_mobile
	- entry_histories_tablet
	- entry_histories_smarttv
	- entry_histories_wearable
	- entry_histories_embedded
	- entry_histories_undefined
*/

CREATE TABLE IF NOT EXISTS entry_histories_console
PARTITION OF entry_histories
FOR VALUES IN ('console');

CREATE TABLE IF NOT EXISTS entry_histories_mobile
PARTITION OF entry_histories
FOR VALUES IN ('mobile');

CREATE TABLE IF NOT EXISTS entry_histories_tablet
PARTITION OF entry_histories
FOR VALUES IN ('tablet');

CREATE TABLE IF NOT EXISTS entry_histories_smarttv
PARTITION OF entry_histories
FOR VALUES IN ('smarttv');

CREATE TABLE IF NOT EXISTS entry_histories_wearable
PARTITION OF entry_histories
FOR VALUES IN ('wearable');

CREATE TABLE IF NOT EXISTS entry_histories_embedded
PARTITION OF entry_histories
FOR VALUES IN ('embedded');

CREATE TABLE IF NOT EXISTS entry_histories_undefined
PARTITION OF entry_histories
FOR VALUES IN ('undefined');