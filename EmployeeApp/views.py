from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage   #HERE WE ARE MAKING USE OF DEFAULT STORAGE MODULE TO SAVE THE FILE

from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer, EmployeeSerializer

# Create your views here.

@csrf_exempt
def departmentAPI (request, id=0): #THIS METHOD WILL RECEIVE AN OPTIONAL ID WHICH WE WILL NEED IN DELETE METHOD (E.G. - ID = 0)
    if request.method == 'GET':  #IN GET METHOD WE WILL RETURN ALL THE RECORDS IN JSON FORMAT.
        departments = Departments.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)  #HERE WE ARE USING SERIALIZER CLASS TO CONVERT IT INTO JSON FORMAT
        return JsonResponse(departments_serializer.data, safe=False)  #THE PARAMETER SAFE = FALSE IS BASICALLY USED TO INFORM DJANGO THAT WHILE WE ARE TRYING TO CONVERT TO JSON IS ACTUALLY A VALID FORMAT AND WE ARE FINE IF THERE ARE STILL ANY ISSUES IN IT.
    elif request.method == 'POST':  #WRITING POST METHOD WHICH WILL BE USED TO INSERT NEW RECORDS INTO DEPARTMENTS TABLE.
        department_data = JSONParser().parse(request)  #WE ARE PARSING THE REQUEST AND USING THE SERIALIZER TO CONVERT IT INTO MODEL.
        departments_serializer = DepartmentSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()  #IF THE MODEL IS VALID WE SAVE IT INTO THE DATABASE
            return JsonResponse('Added successfully', safe=False)  # AND RETURN SUCCESS MESSAGE.
        return JsonResponse('Failed to add!',safe=False)
    elif request.method == 'PUT': # IT WILL BE USED FOR UPDATING A VALUE.
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(DepartmentId = department_data['DepartmentId'])    #FIRST WE ARE CAPTURING THE EXISTING RECORD USING DEPARTMENT ID
        departments_serializer = DepartmentSerializer(department, data=department_data) #NEXT WE ARE MAPPING IT WITH NEW VALUES, USING SERIALIZER CLASS.
        if departments_serializer.is_valid():
            departments_serializer.save()   #AND SAVING IT IF THE MODEL IS VALID.
            return JsonResponse('Updated successfully',safe=False)
        return JsonResponse('Failed to update!',safe=False)
    elif request.method == 'DELETE': #IMPLEMENTING THE DELETE METHOD.
        department = Departments.objects.get(DepartmentId = id) #WE WILL BE PASING THE ID HERE TO BE DELETED FROM THE URL.
        department.delete()
        return JsonResponse('Deleted successfully',safe=False)


@csrf_exempt
def employeeAPI(request, id=0):
    if request.method == 'GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data,safe=False)
    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse('Employee Added Successfully',safe=False)
        return JsonResponse('Failed to add!',safe=False)
    elif request.method == 'PUT':
        employee_data = JSONParser().parse(request)
        employee = Employees.objects.get(EmployeeId = employee_data['EmployeeId'])
        employees_serializer = EmployeeSerializer(employee, data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse('Employee updated successfully',safe=False)
        return JsonResponse('Failed to update!',safe=False)
    elif request.method == 'DELETE':
        employee = Employees.objects.get(EmployeeId = id)
        employee.delete()
        return JsonResponse('Employee deleted successfully',safe=False)


@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)