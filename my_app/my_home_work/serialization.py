from marshmallow import Schema, fields, ValidationError, validate


class LearnerSchema(Schema):
    uid = fields.Integer(required=True, strict=True, validate=validate.Range(min=1, error="UID должен быть положительным числом"))
    name = fields.String(
        required=True,
        validate=validate.Length(min=3, error="Для имени нужно не менее трех букв")
    )
    final_test = fields.Boolean(required=True)

if __name__ == "__main__":
    schema = LearnerSchema()

    print("Сериализация экзмемпляра модели в словарь")
    learner_data = {'uid': 10, 'name': 'Vlad', 'final_test': True}
    result = schema.dump(learner_data)
    print(result)
   
    print("Десериализация единичного экземпляра")
    loaded = schema.load(learner_data)
    print(loaded)
  
    print("Сериализация списка экземпляров")
    learners_list = [
        {'uid': 1, 'name': 'Alice', 'final_test': True},
        {'uid': 2, 'name': 'Bob', 'final_test': False}
    ]
    result_list = schema.dump(learners_list, many=True)
    print(result_list)

    print("Десериализация списка экземпляров")
    loaded_list = schema.load(learners_list, many=True)
    print(loaded_list)
    
    print("Проверка валидации")
    invalid_data = {'uid': -5, 'name': 'A', 'final_test': True}
    try:
        schema.load(invalid_data)
    except ValidationError as e:
        print(f"Ошибка: {e.messages}")