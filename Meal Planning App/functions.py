import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()  
openai.api_key = os.getenv("API_KEY")  

def generate_menu(diet_type, num_days, meals_per_day):
    """
    Genera un menú semanal basado en las preferencias del usuario.

    Esta función utiliza la API de OpenAI para obtener un menú semanal basado en las
    preferencias del usuario. El menú se genera con la cantidad de días y comidas
    al día especificadas por el usuario.

    Args:
        diet_type (str): El tipo de dieta para la que se va a generar el menú.
        num_days (int): El número de días que tendrá el menú.
        meals_per_day (int): El número de comidas al día que tendrá el menú.

    Retorna:
        str: El menú generado.
    """
    prompt = (f"Genera un menú semanal de {num_days} días para una persona que sigue una dieta {diet_type}, "
              f"con {meals_per_day} comidas al día. Asegúrate de incluir comidas variadas y balanceadas.")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error al generar el menú: {str(e)}")
        return None

def save_menu(menu, filename="menu_semanal.txt"):
    """Guarda el menú en un archivo de texto.

    Esta función guarda el menú en un archivo de texto con el nombre especificado.
    Si el archivo no existe, se crea. Si el archivo ya existe, se reemplaza su contenido.

    Args:
        menu (str): El contenido del menú que se va a guardar.
        filename (str): El nombre del archivo donde se va a guardar el menú. Por defecto,
            se utiliza el nombre 'menu_semanal.txt'.
    """
    try:
        with open(filename, 'w') as file:
            file.write(menu)
        print(f"Menú guardado en '{filename}'.")
        run_conversation()
    except Exception as e:
        print(f"Error al guardar el menú: {str(e)}")

def load_menu(filename="menu_semanal.txt"):
    """Carga un menú guardado en un archivo de texto.

    Esta función carga un menú previamente guardado en un archivo de texto
    y lo muestra en la consola. Si el archivo no existe, la función devuelve
    None.

    Args:
        filename (str): El nombre del archivo que contiene el menú. Por defecto,
            se utiliza el nombre 'menu_semanal.txt'.
    """
    try:
        with open(filename, 'r') as file:
            menu = file.read()
        clear_screen()
        print("Menú cargado:\n")
        print(menu)
        return menu
    except FileNotFoundError:
        print(f"El archivo '{filename}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error al cargar el menú: {str(e)}")
        return None


def suggest_recipes(diet_type):
    """Sugiere recetas según el tipo de dieta.

    Esta función utiliza la API de OpenAI para obtener sugerencias de recetas
    basadas en el tipo de dieta proporcionado por el usuario.

    Args:
        diet_type (str): El tipo de dieta para la que se sugieren recetas.

    Retorna:
        str: Las recetas sugeridas para el tipo de dieta especificado.
    """
    prompt = f"Sugiere algunas recetas para una dieta {diet_type}."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error al obtener recetas: {str(e)}")
        return None

def run_conversation():
    """Ejecuta la conversación y genera un menú basado en las preferencias del usuario.

    Pide al usuario que introduzca el tipo de dieta, el número de días y el número
    de comidas al día. Luego, utilizando la función generate_menu, genera un menú
    personalizado y lo devuelve.

    Retorna:
        str: El menú personalizado generado.
    """
    try:
        # Pedir al usuario que introduzca el tipo de dieta
        diet_type = input("Introduce el tipo de dieta (vegetariana, vegana, sin gluten, etc.): ")

        # Pedir al usuario que introduzca el número de días
        num_days = int(input("Introduce el número de días (3, 5 o 7): "))

        # Pedir al usuario que introduzca el número de comidas al día
        meals_per_day = int(input("Introduce el número de comidas al día (1, 2 o 3): "))

        # Generar el menú
        menu = generate_menu(diet_type, num_days, meals_per_day)
        
        if menu:
            # Mostrar el menú
            print("\nAquí tienes tu menú semanal:\n")
            print(menu)
            return menu
        else:
            print("No se pudo generar el menú.")
            return None
    except ValueError:
        # Mostrar un error si el usuario introduce un valor no válido
        print("Por favor, introduce un número válido para los días y las comidas.")
        return None

def interactive_menu():
    """Proporciona un menú interactivo para el usuario.

    El menú interactivo permite al usuario interactuar con el programa de varias formas:
        1. Generar un nuevo menú
        2. Guardar menú
        3. Cargar menú
        4. Sugerir recetas
        5. Salir
    """
    while True:
        # Mostrar las opciones del menú
        print("\nOpciones:")
        print("1. Generar un nuevo menú")
        print("2. Guardar menú")
        print("3. Cargar menú")
        print("4. Sugerir recetas")
        print("5. Salir")

        # Pedir al usuario que elija una opción
        choice = input("Elige una opción (1-5): ")

        if choice == '1':
            # Generar un nuevo menú
            run_conversation()
        elif choice == '2':
            # Guardar el menú generado
            menu = run_conversation()  # Llama a la función para generar el menú
            if menu:
                save_menu(menu)
        elif choice == '3':
            # Cargar un menú desde un archivo
            load_menu()
        elif choice == '4':
            # Sugerir recetas según el tipo de dieta
            diet_type = input("Introduce el tipo de dieta para las recetas: ")
            recipes = suggest_recipes(diet_type)
            if recipes:
                print("\nRecetas sugeridas:\n")
                print(recipes)
        elif choice == '5':
            # Salir del programa
            print("Saliendo del programa.")
            break
        else:
            # Opción no válida
            print("Opción no válida. Por favor, elige otra.")
            
def clear_screen():
    os.system('cls')
