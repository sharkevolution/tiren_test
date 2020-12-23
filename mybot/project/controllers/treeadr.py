
import logging


def show_city(tree_city, chat_id, name_ord):

    for b in tree_city:
        if name_ord in b[1]:
            access = b[2]
            if chat_id in access:
                pass
            else:
                access.append(chat_id)
                b[2] = access

    return tree_city
