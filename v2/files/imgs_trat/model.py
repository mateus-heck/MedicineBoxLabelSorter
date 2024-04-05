from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


# Diretório contendo as imagens de treinamento
diretorio_treinamento = 'imgs_trat\imgs'

# Diretório contendo as imagens de validação
diretorio_validacao = r'imgs_trat\valid_imgs'

# Configuração do ImageDataGenerator para pré-processamento de dados
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normaliza os valores dos pixels para o intervalo [0, 1]
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Configuração do ImageDataGenerator para dados de validação (apenas rescaling)
validation_datagen = ImageDataGenerator(rescale=1./255)

# Carrega e pré-processa as imagens de treinamento em lotes
train_generator = train_datagen.flow_from_directory(
    diretorio_treinamento,  # Diretório contendo as imagens de treinamento
    target_size=(400, 200),  # Redimensiona as imagens para o tamanho desejado
    batch_size=1,
    class_mode='binary'  # Modo de classificação binária (certa/errada)
)

# Carrega e pré-processa as imagens de validação em lotes
validation_generator = validation_datagen.flow_from_directory(
    diretorio_validacao,  # Diretório contendo as imagens de validação
    target_size=(400, 200),  # Redimensiona as imagens para o tamanho desejado
    batch_size=1,
    class_mode='binary'  # Modo de classificação binária (certa/errada)
)


# Defina a arquitetura do modelo
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(400, 200, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# Compile o modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Treine o modelo
history = model.fit(
    train_generator,
    epochs=100,
    validation_data=train_generator
)

model.save('modelo_1_90.h5')