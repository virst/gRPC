# gRPC

## Тестовое демо

## C#

### Определение сервиса
####  greet.proto

``` protobuf
syntax = "proto3";
 
option csharp_namespace = "GreeterServiceApp";
 
package greet;
 
// определение сервиса
service Greeter {
  // отправка сообщения
  rpc SayHello (HelloRequest) returns (HelloReply);
}
 
// сообщение от клиента содержит name
message HelloRequest {
  string name = 1;
}
 
// сообщение клиенту содержит message
message HelloReply {
  string message = 1;
}
```

### Реализация сервиса

В папке Services по умолчанию в файле GreeterService.cs определен класс GreeterService, который представляет реализацию сервиса gPRC на языке C#:

``` csharp
using Grpc.Core;
using GreeterServiceApp;
 
namespace GreeterServiceApp.Services;
 
public class GreeterService : Greeter.GreeterBase
{
    private readonly ILogger<GreeterService> _logger;
    public GreeterService(ILogger<GreeterService> logger)
    {
        _logger = logger;
    }
 
    public override Task<HelloReply> SayHello(HelloRequest request, ServerCallContext context)
    {
        return Task.FromResult(new HelloReply
        {
            Message = "Hello " + request.Name
        });
    }
}
```

Класс сервиса (в данном случае GreeterService) наследуется от класса Greeter.GreeterBase. Greeter.GreeterBase - абстрактный класс, который автоматически генерируется по определению сервиса greeter в файле greeter.proto.

Класс GreeterService по сути представляет обычный класс C#. Так, по умолчанию он имеет конструктор, который посредством dependency injection получает объект логгера и может его использовать для логирования.

### Подключение gRPC
Точкой входа в программу по умолчанию является класс Program, который определен неявно в файле Program.cs. И имеено здесь и происходит подключение всей инфраструктуры gRPC:
``` csharp
using GreeterServiceApp.Services;
 
var builder = WebApplication.CreateBuilder(args);
 
// добавляем сервисы для работы с gRPC
builder.Services.AddGrpc();
 
var app = builder.Build();
 
// настраиваем обработку HTTP-запросов
app.MapGrpcService<GreeterService>();
app.MapGet("/", () => "Communication with gRPC endpoints must be made through a gRPC client...");
 
app.Run();
```

### Клиент для gRPC-сервиса

файл проекта будет выглядеть следующим образом:

``` xml
<Project Sdk="Microsoft.NET.Sdk">
 
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
 
  <ItemGroup>
    <Protobuf Include="Protos\greet.proto" GrpcServices="Client" />
  </ItemGroup>
 
  <ItemGroup>
    <PackageReference Include="Google.Protobuf" Version="3.25.1" />
    <PackageReference Include="Grpc.Net.Client" Version="2.59.0" />
    <PackageReference Include="Grpc.Tools" Version="2.59.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
  </ItemGroup>
 
</Project>
```

#### Определение кода клиента
Далее в проекте консольного клиента изменим код файла Program.cs следующим образом:

``` csharp
using Grpc.Net.Client;
using GreeterClientApp;
 
// создаем канал для обмена сообщениями с сервером
// параметр - адрес сервера gRPC
using var channel = GrpcChannel.ForAddress("http://localhost:5134");
// создаем клиент
var client = new Greeter.GreeterClient(channel);
Console.Write("Введите имя: ");
string? name = Console.ReadLine();
// обмениваемся сообщениями с сервером
var reply = await client.SayHelloAsync(new HelloRequest { Name = name });
Console.WriteLine($"Ответ сервера: {reply.Message}");
Console.ReadKey();
```

### Python Demo

#### Generate gRPC code
Next we need to update the gRPC code used by our application to use the new service definition.

From the examples/python/helloworld directory, run:
```
$ python -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/helloworld.proto
```
This regenerates helloworld_pb2.py which contains our generated request and response classes and helloworld_pb2_grpc.py which contains our generated client and server classes.

#### Update the client
In the same directory, open greeter_client.py. Call the new method like this:

``` python
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
```
