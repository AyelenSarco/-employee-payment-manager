from src.core.service.service_rol import create_rol
from src.core.service.service_permisson import create_permisson
from src.core.service.service_user import create_user
from src.core.service.service_employee import create_employee
from src.core.service.service_payment import create_payment
from datetime import datetime

def run():

    # ROLES CREATION
    rol1_administrator = create_rol(name="Administrator")
    rol2_viewer = create_rol(name="Viewer")

    # PERMISSONS

    # users
    user_create = create_permisson(name="user_create")
    user_edit = create_permisson(name="user_edit")
    user_delete = create_permisson(name="user_delete")
    user_view = create_permisson(name="user_view")
    user_list = create_permisson(name="user_list")

    # employees

    employee_create = create_permisson(name="employee_create")
    employee_edit = create_permisson(name="employee_edit")
    employee_delete = create_permisson(name="employee_delete")
    employee_view = create_permisson(name="employee_view")
    employee_list = create_permisson(name="employee_list")

    # payments
    payment_create = create_permisson(name="payment_create")
    payment_delete = create_permisson(name="payment_delete")
    payment_view = create_permisson(name="payment_view")
    payment_list = create_permisson(name="payment_list")

    # ADMINISTRATOR ROL --> all 
    rol1_administrator.permissons.append(user_create)
    rol1_administrator.permissons.append(user_edit)
    rol1_administrator.permissons.append(user_delete)
    rol1_administrator.permissons.append(user_view)
    rol1_administrator.permissons.append(user_list)
    rol1_administrator.permissons.append(employee_create)
    rol1_administrator.permissons.append(employee_edit)
    rol1_administrator.permissons.append(employee_delete)
    rol1_administrator.permissons.append(employee_view)
    rol1_administrator.permissons.append(employee_list)
    rol1_administrator.permissons.append(payment_create)
    rol1_administrator.permissons.append(payment_delete)
    rol1_administrator.permissons.append(payment_view)
    rol1_administrator.permissons.append(payment_list)

    # VIEWER --> only view and list
    rol2_viewer.permissons.append(user_view)
    rol2_viewer.permissons.append(user_list)
    rol2_viewer.permissons.append(employee_view)
    rol2_viewer.permissons.append(employee_list)
    rol2_viewer.permissons.append(payment_view)
    rol2_viewer.permissons.append(payment_list)

    # ---------------------------------------------------------

    user_sys = create_user (
        name = 'SysAdmin',
        email = 'sys_admin@mail.com',
        hashed_password = '1234',
        is_active = True,
        #creation_date = datetime(2025, 1, 10),
        sys_admin = True,
        rol = rol1_administrator
    )

    user_admin = create_user (
        name = 'Administrator',
        email = 'administrator_only@mail.com',
        hashed_password = '1234',
        is_active = True,
        creation_date = datetime(2025, 1, 15),
        sys_admin = False,
        rol = rol1_administrator
    )

    user_viewer = create_user (
        name = 'Viewer',
        email = 'viewer@mail.com',
        hashed_password = '1234',
        is_active = True,
        creation_date = datetime(2025, 1, 20),
        sys_admin = False,
        rol = rol2_viewer
    )

    # two payments (salary and bonus)
    employee_1 = create_employee(
        dni = '11111111',
        name = 'Francisco Caballa',
        email = 'francisco@mail.com',
        is_active = True
    )

    # two payments (salary and bonus)
    employee_2 = create_employee(
        dni = '22222222',
        name = 'Camila Perone',
        email = 'camila@mail.com',
        is_active = True
    )

    # without payments yet
    employee_3 = create_employee(
        dni = '33333333',
        name = 'Juliet Stev',
        email = 'juliet@mail.com',
        is_active = True
    )


    payment_e1_1 = create_payment(
        amount = 1000.5,
        date= datetime(2025,1,1),
        payment_type = 'Salary',
        description = 'Francisco first salary',
        employee = employee_1
    )

    payment_e1_2 = create_payment(
        amount = 500,
        date= datetime(2025,5,1),
        payment_type = 'Bonus',
        description = 'Francisco first bonus',
        employee = employee_1
    )

    payment_e2_1 = create_payment(
        amount = 1200.5,
        date= datetime(2025,1,1),
        payment_type = 'Salary',
        description = 'Camila first salary',
        employee = employee_2
    )

    payment_e2_1 = create_payment(
        amount = 500,
        date= datetime(2025,5,1),
        payment_type = 'Bonus',
        description = 'Camila first bonus',
        employee = employee_2
    )

    expense_payment = create_payment(
        amount = 200,
        date= datetime(2025,1,1),
        payment_type = 'Expense',
        description = 'Paper suppliers',
    )
