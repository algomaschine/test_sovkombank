для Golang версии надо сделать билд вот таким образом, чтобы появился экзешник или переименовать megatrader в mehatrader.exe:
go build .\megatrader.go
либо запустить тут https://www.programiz.com/golang/online-compiler/

бинарник под платформму Windows доступен по ссылке https://www.dropbox.com/scl/fi/zn7ai4rtj008lvg8hm8bt/megatrader.zip?rlkey=o6h9l3ybq90rrm9ytl222yhkv&st=e0ypchtp&dl=0

эта версия будет работать более оптимально, тк использует функциональное программирование и многопоточность

TODO: я думаю ту нам не хватает визуализации unrealized/realized pnl и купленных объемов, по вашему запросу я бы с удовольствием её добавил.

С уважением, 
Эдуард Самохвалов

edward.samokhvalov@gmail.com