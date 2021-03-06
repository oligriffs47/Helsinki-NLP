from keras.preprocessing.text import Tokenizer

corpus = open("data/cleaned/summaries.txt").read().splitlines()

tokenizer = Tokenizer()


def get_sequence_of_tokens(corpus):
    # tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1

    # convert data to sequence of tokens
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words


inp_sequences, total_words = get_sequence_of_tokens(corpus)
print(len(inp_sequences))


def generate_padded_sequences(input_sequences):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = keras.utils.np_utils.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len


predictors, label, max_sequence_len = generate_padded_sequences(inp_sequences)


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()

    # Add Input Embedding Layer
    model.add(Embedding(total_words, 10, input_length=input_len))

    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(60))
    model.add(Dropout(0.1))

    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


model = create_model(max_sequence_len, total_words)
model.summary()

model.fit(predictors, label, epochs=20, verbose=5)


def generate_text(seed_text, next_words, model, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = model.predict(token_list, verbose=0)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            '''
            if index == predicted:
                output_word = word
                break
            '''
        seed_text += " " + word
    return seed_text.title()


print (generate_text("zergrg ergreg", 15, model, max_sequence_len))
