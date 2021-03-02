import logging


def show_city(tree_city, chat_id, name_ord):
    single_quote = '\''
    city_name = name_ord.split(f"{single_quote}")

    logging.info(city_name)

    for b in tree_city:
        if city_name[1] in b[1]:
            access = b[2]
            if chat_id in access:
                pass
            else:
                access.append(chat_id)
                b[2] = access

    return tree_city


def hide_city(tree_city, chat_id, name_ord):
    single_quote = '\''
    city_name = name_ord.split(f"{single_quote}")

    logging.info(city_name)

    for b in tree_city:
        if city_name[1] in b[1]:
            access = b[2]
            if chat_id in access:
                access.remove(chat_id)
                b[2] = access
            else:
                pass

    return tree_city


def delete_address(tree_adr, chat_id, name_ord):
    single_quote = '\''
    adr_name = name_ord.split(f"{single_quote}")

    logging.info(adr_name)

    for b in tree_adr:
        if adr_name[1] in b[2]:
            tree_adr.remove(b)
            break

    return tree_adr


def delete_city(tree_city, chat_id, name_ord):
    single_quote = '\''
    city_name = name_ord.split(f"{single_quote}")

    logging.info(f'Try delete {city_name}')

    for b in tree_city:
        if city_name[1] in b[1]:
            tree_city.remove(b)
            logging.info(f'Removed {b}')
            break

    return tree_city
