import pytest
from students.models import Course


@pytest.mark.django_db
def test_get_one(client, data_factory):
    """Проверка получения 1го курса"""
    # Arrange
    student_set = data_factory('Student', _quantity=1)
    course = data_factory('Course', make_m2m=True, _quantity=1, students=student_set)
    # Act
    response = client.get('/api/v1/courses/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    assert data[0]['name'] == course[0].name


@pytest.mark.django_db
def test_get_many(client, data_factory):
    """Проверка получения списка курсов"""
    # Arrange
    student_set = data_factory('Student', _quantity=3)
    course = data_factory('Course', make_m2m=True, _quantity=5, students=student_set)
    # Act
    response = client.get('/api/v1/courses/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    for i, c in enumerate(data):
        assert c['name'] == course[i].name

@pytest.mark.django_db
def test_filter_id(client, data_factory):
    """Проверка фильтрации списка курсов по id"""
    # Arrange
    student_set = data_factory('Student', _quantity=1)
    course = data_factory('Course', make_m2m=True, _quantity=10, students=student_set)
    # Act
    response = client.get('/api/v1/courses/?id=2')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[1].name


@pytest.mark.django_db
def test_filter_id(client, data_factory):
    """Проверка фильтрации списка курсов по name курса"""
    # Arrange
    student_set = data_factory('Student', _quantity=3)
    course = data_factory('Course', make_m2m=True, _quantity=10, students=student_set)
    c = course[2].name
    s = student_set[0]
    # Act
    response = client.get(f'/api/v1/courses/?name={c}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course[2].name


@pytest.mark.django_db
def test_create_course(client):
    """Тест успешного создания курса"""
    # Arrange
    count = Course.objects.count()
    # Act
    response = client.post('/api/v1/courses/', data={'name': 'Математика'})
    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update(client, data_factory):
    """Тест успешного обновления курса"""
    # Arrange
    student_set = data_factory('Student', _quantity=1)
    course = data_factory('Course', make_m2m=True, _quantity=3, students=student_set)
    # Act
    response = client.patch('/api/v1/courses/1/',  data={'name': 'Математика'})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Математика'


@pytest.mark.django_db
def test_delete(client, data_factory):
    """Тест успешного удаления курса"""
    # Arrange
    student_set = data_factory('Student', _quantity=1)
    course = data_factory('Course', make_m2m=True, _quantity=3, students=student_set)
    count = Course.objects.count()
    # Act
    response = client.delete('/api/v1/courses/1/')
    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == count - 1

