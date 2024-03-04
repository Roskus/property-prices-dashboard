# Property prices Dashboard
import json
import pandas as pd


def flatten_coordinates(coordinates):
    return coordinates['latitude'], coordinates['longitude']


def extract_feature_value(features, key):
    for feature in features:
        if feature['key'] == key:
            return int(feature['value'][0]) if feature[
                'value'] else 0  # Convertir a entero si hay un valor, de lo contrario, 0
    return 0


def parse_json(file):
    with open(file) as f:
        data = json.load(f)

    return data['propertyCoordinates']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Parsear los datos de alquiler de Barcelona y Madrid
    barcelona_rent = parse_json('data/rent/barcelona.json')
    madrid_rent = parse_json('data/rent/madrid.json')

    # Parsear los datos de compra de Barcelona y Madrid
    barcelona_purchase = parse_json('data/purchase/barcelona.json')
    madrid_purchase = parse_json('data/purchase/madrid.json')

    # Crear DataFrames de pandas para cada conjunto de datos
    df_barcelona_rent = pd.DataFrame(barcelona_rent)
    df_madrid_rent = pd.DataFrame(madrid_rent)
    df_barcelona_purchase = pd.DataFrame(barcelona_purchase)
    df_madrid_purchase = pd.DataFrame(madrid_purchase)

    # Agregar una columna para identificar la ciudad y el tipo de operación
    df_barcelona_rent['city'] = 'Barcelona'
    df_madrid_rent['city'] = 'Madrid'
    df_barcelona_purchase['city'] = 'Barcelona'
    df_madrid_purchase['city'] = 'Madrid'

    df_barcelona_rent['operation'] = 'rent'
    df_madrid_rent['operation'] = 'rent'
    df_barcelona_purchase['operation'] = 'purchase'
    df_madrid_purchase['operation'] = 'purchase'

    # Concatenar todos los DataFrames en uno solo
    df = pd.concat([df_barcelona_rent, df_madrid_rent, df_barcelona_purchase, df_madrid_purchase])

    # Eliminar las filas con precio 0 o nulo
    df = df[df['price'] != 0]
    df = df.dropna(subset=['price'])

    # Aplanar la columna de coordenadas
    df['latitude'], df['longitude'] = zip(*df['coordinates'].apply(flatten_coordinates))

    # Aplanar la columna de características ('features') y extraer los valores específicos
    df['surface'] = df['features'].apply(lambda x: extract_feature_value(x, 'surface'))
    df['elevator'] = df['features'].apply(lambda x: extract_feature_value(x, 'elevator'))
    df['rooms'] = df['features'].apply(lambda x: extract_feature_value(x, 'rooms'))
    df['parking'] = df['features'].apply(lambda x: extract_feature_value(x, 'parking'))

    # Reordenar las columnas si es necesario
    df = df[['price', 'latitude', 'longitude', 'city', 'operation', 'surface', 'rooms', 'elevator', 'parking']]

    # Mostrar las primeras filas del DataFrame para verificar la estructura
    print(df.head())

    df.to_csv('data/export/data_for_dashboard.csv', index=False)
