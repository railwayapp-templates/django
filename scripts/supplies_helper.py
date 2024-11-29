maping = [
    {
        "heading": "Incontinent Supplies Taken and Quantity  [#6 Bladder pads  (27 per package)]",
        "id": 29
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [#4 Bladder pads (18 per package)]",
        "id": 28
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XXL Pull ups - Women  (12 per package)]",
        "id": 27
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XXL tabs - Women (12 per package)]",
        "id": 26
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XL Pull ups - Women  (14 per package)]",
        "id": 25
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XL tabs -Women  (14 per package)]",
        "id": 24
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [L Pull ups - Women (18 per package)]",
        "id": 23
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [L tabs - Women (18 per package)]",
        "id": 22
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [M Pull ups -Women  (20 per package)]",
        "id": 21
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [M tabs - Women (20 per package)]",
        "id": 20
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S/M Pull ups - Women (20 per package)]",
        "id": 19
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S/M tabs - Women (20 per package)]",
        "id": 18
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S Pull ups - Women (20 per package)]",
        "id": 17
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S tabs – Women  (20 per package)]",
        "id": 16
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [Men's Guards (18 per package)]",
        "id": 15
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XXL Pull ups - Men  (12 per package)]",
        "id": 14
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XXL tabs - Men (12 per package)]",
        "id": 13
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XL Pull ups - Men (14 per package)]",
        "id": 12
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [XL tabs -Men  (14 per package)]",
        "id": 11
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [L Pull ups - Men (18 per package)]",
        "id": 10
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [L tabs - Men (18 per package)]",
        "id": 9
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [M Pull ups - Men  (20 per package)]",
        "id": 8
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [M tabs - Men  (20 per package)]",
        "id": 7
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S/M Pull ups - Men (20 per package)]",
        "id": 6
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S/M tabs - Men (20 per package)]",
        "id": 5
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S Pull ups - Men (20 per package)]",
        "id": 4
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [S tabs – Men  (20 per package)]",
        "id": 3
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [Bed pads  (each)]",
        "id": 2
    },
    {
        "heading": "Incontinent Supplies Taken and Quantity  [Wipes (20 per package)]",
        "id": 1
    }
]

# Supplies mapping helper functions
def get_supplies_id(heading):
    for item in maping:
        if item["heading"] == heading:
            return item["id"]
    return None
