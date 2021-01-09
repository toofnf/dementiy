def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    k = [x for x in keyword]  # массив букв пароля
    p = [y for y in plaintext]  # массив букв изначального слова
    for i in range(len(p)):  # пробегаем по начальному слову
        if len(k) < len(p):  # пароль короче слова
            if (i + 1) % len(k) == 0:  # если это последняя буква, то
                if 64 < ord(k[len(k) - 1]) < 91:  # буква ключа заглавная
                    if (64 < ord(p[i]) < 91 + 65 - ord(k[len(k) - 1])) or (96 < ord(p[i]) < 123 + 65 - ord(
                            k[len(k) - 1])):  # если буква при сдвиге не прокручивается в начало цикла
                        p[i] = chr(ord(p[i]) + ord(k[len(k) - 1]) - 65)  # букавка обновилась
                    elif 90 + 65 - ord(k[len(k) - 1]) < ord(p[i]) < 91 or 122 + 65 - ord(k[len(k) - 1]) < ord(
                            p[i]) < 123:  # если буковка прокручивается в начало списка
                        p[i] = chr(ord(k[len(k) - 1]) - 65 - 26 + ord(p[i]))  # буковка обновилась
                elif 96 < ord(k[len(k) - 1]) < 123:  # буква ключа строчная
                    if (64 < ord(p[i]) < 91 + 91 - ord(k[len(k) - 1])) or (
                            96 < ord(p[i]) < 123 + 91 - ord(k[len(k) - 1])):  # если буква не переходит в новый цикл
                        p[i] = chr(ord(p[i]) + ord(k[len(k) - 1]) - 97)  # обновление буквы
                    elif 91 + 96 - ord(k[len(k) - 1]) < ord(p[i]) < 91 or 96 + 123 - ord(k[len(k) - 1]) < ord(
                            p[i]) < 123:  # если буква переходит в начало цикла
                        p[i] = chr(ord(k[len(k) - 1]) - 97 - 26 + ord(p[i]))  # буковка обновилась
            else:  # буква не последняя
                if 64 < ord(k[i % len(k)]) < 91:  # буква ключа заглавная
                    if (64 < ord(p[i]) < 91 + 65 - ord(k[i % len(k)])) or (
                            96 < ord(p[i]) < 123 + 65 - ord(k[i % len(k)])):
                        p[i] = chr(ord(p[i]) + ord(k[i % len(k)]) - 65)
                    elif 90 + 65 - ord(k[i % len(k)]) < ord(p[i]) < 91 or 122 + 65 - ord(k[i % len(k)]) < ord(
                            p[i]) < 123:
                        p[i] = chr(ord(k[i % len(k)]) - 65 - 26 + ord(p[i]))
                elif 96 < ord(k[i % len(k)]) < 123:  # буква ключа строчная
                    if (64 < ord(p[i]) < 91 + 91 - ord(k[i % len(k)])) or (
                            96 < ord(p[i]) < 123 + 91 - ord(k[i % len(k)])):
                        p[i] = chr(ord(p[i]) + ord(k[i % len(k)]) - 97)
                    elif 91 + 96 - ord(k[i % len(k)]) < ord(p[i]) < 91 or 123 + 96 - ord(k[i % len(k)]) < ord(
                            p[i]) < 123:
                        p[i] = chr(ord(k[i % len(k)]) - 97 - 26 + ord(p[i]))
        elif len(k) >= len(p):  # пароль длиннее или равен длине слова
            if 64 < ord(k[i]) < 91:
                if (64 < ord(p[i]) < 91 + 65 - ord(k[i])) or (96 < ord(p[i]) < 123 + 65 - ord(k[i])):
                    p[i] = chr(ord(p[i]) + ord(k[i]) - 65)
                elif 90 + 65 - ord(k[i]) < ord(p[i]) < 91 or 122 + 65 - ord(k[i]) < ord(p[i]) < 123:
                    p[i] = chr(ord(k[i]) - 65 - 26 + ord(p[i]))
            elif 96 < ord(k[i]) < 123:
                if (64 < ord(p[i]) < 91 + 91 - ord(k[i])) or (96 < ord(p[i]) < 123 + 91 - ord(k[i])):
                    p[i] = chr(ord(p[i]) + ord(k[i]) - 97)
                elif 91 + 96 - ord(k[i]) < ord(p[i]) < 91 or 123 + 96 - ord(k[i]) < ord(p[i]) < 123:
                    p[i] = chr(ord(k[i]) - 97 - 26 + ord(p[i]))
    return ciphertext.join(p)

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    k = [x for x in keyword]
    p = [y for y in ciphertext]
    for i in range(len(p)):  # пробегаем по начальному слову
        if len(k) < len(p):  # пароль короче слова
            if (i + 1) % len(k) == 0:  # если это последняя буква, то
                if 64 < ord(k[len(k) - 1]) < 91:  # буква ключа заглавная
                    if ord(k[len(k) - 1]) - 1 < ord(p[i]) < 91 or ord(k[len(k) - 1]) + 31 < ord(
                            p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                        p[i] = chr(ord(p[i]) - ord(k[len(k) - 1]) + 65)  # букавка обновилась
                    elif 64 < ord(p[i]) < ord(k[len(k) - 1]) or 96 < ord(p[i]) < ord(
                            k[len(k) - 1]) + 32:  # если буковка прокручивается в начало списка
                        p[i] = chr(ord(p[i]) - ord(k[len(k) - 1]) + 65 + 26)  # буковка обновилась
                elif 96 < ord(k[len(k) - 1]) < 123:  # буква ключа строчная
                    if ord(k[len(k) - 1]) - 33 < ord(p[i]) < 91 or ord(k[len(k) - 1]) < ord(
                            p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                        p[i] = chr(ord(p[i]) - ord(k[len(k) - 1]) + 97)  # букавка обновилась
                    elif 64 < ord(p[i]) < ord(k[len(k) - 1]) - 32 or 96 < ord(p[i]) < ord(
                            k[len(k) - 1]):  # если буковка прокручивается в начало списка
                        p[i] = chr(ord(p[i]) - ord(k[len(k) - 1]) + 97 + 26)  # буковка обновилась
            else:  # буква не последняя
                if 64 < ord(k[i % len(k)]) < 91:  # буква ключа заглавная
                    if ord(k[i % len(k)]) - 1 < ord(p[i]) < 91 or ord(k[i % len(k)]) + 31 < ord(
                            p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                        p[i] = chr(ord(p[i]) - ord(k[i % len(k)]) + 65)  # букавка обновилась
                    elif 64 < ord(p[i]) < ord(k[i % len(k)]) or 96 < ord(p[i]) < ord(
                            k[i % len(k)]) + 32:  # если буковка прокручивается в начало списка
                        p[i] = chr(ord(p[i]) - ord(k[i % len(k)]) + 65 + 26)  # буковка обновилась
                elif 96 < ord(k[i % len(k)]) < 123:  # буква ключа строчная
                    if ord(k[i % len(k)]) - 33 < ord(p[i]) < 91 or ord(k[i % len(k)]) < ord(
                            p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                        p[i] = chr(ord(p[i]) - ord(k[i % len(k)]) + 97)  # букавка обновилась
                    elif 64 < ord(p[i]) < ord(k[i % len(k)]) - 32 or 96 < ord(p[i]) < ord(
                            k[i % len(k)]):  # если буковка прокручивается в начало списка
                        p[i] = chr(ord(p[i]) - ord(k[i % len(k)]) + 97 + 26)  # буковка обновилась
        elif len(k) >= len(p):  # пароль длиннее или равен длине слова
            if 64 < ord(k[i % len(k)]) < 91:  # буква ключа заглавная
                if ord(k[i]) - 1 < ord(p[i]) < 91 or ord(k[i]) + 31 < ord(
                        p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                    p[i] = chr(ord(p[i]) - ord(k[i]) + 65)  # букавка обновилась
                elif 64 < ord(p[i]) < ord(k[i]) or 96 < ord(p[i]) < ord(
                        k[i]) + 32:  # если буковка прокручивается в начало списка
                    p[i] = chr(ord(p[i]) - ord(k[i]) + 65 + 26)  # буковка обновилась
            elif 96 < ord(k[i]) < 123:  # буква ключа строчная
                if ord(k[i]) - 33 < ord(p[i]) < 91 or ord(k[i]) < ord(
                        p[i]) < 123:  # если буква при сдвиге не прокручивается в начало цикла
                    p[i] = chr(ord(p[i]) - ord(k[i]) + 97)  # букавка обновилась
                elif 64 < ord(p[i]) < ord(k[i]) - 32 or 96 < ord(p[i]) < ord(
                        k[i]):  # если буковка прокручивается в начало списка
                    p[i] = chr(ord(p[i]) - ord(k[i]) + 97 + 26)  # буковка обновилась
    return plaintext.join(p)
