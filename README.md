# gRPC

## �������� ����

## C#

### ����������� �������
####  greet.proto

``` protobuf
syntax = "proto3";
 
option csharp_namespace = "GreeterServiceApp";
 
package greet;
 
// ����������� �������
service Greeter {
  // �������� ���������
  rpc SayHello (HelloRequest) returns (HelloReply);
}
 
// ��������� �� ������� �������� name
message HelloRequest {
  string name = 1;
}
 
// ��������� ������� �������� message
message HelloReply {
  string message = 1;
}
```

### ���������� �������

� ����� Services �� ��������� � ����� GreeterService.cs ��������� ����� GreeterService, ������� ������������ ���������� ������� gPRC �� ����� C#:

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

����� ������� (� ������ ������ GreeterService) ����������� �� ������ Greeter.GreeterBase. Greeter.GreeterBase - ����������� �����, ������� ������������� ������������ �� ����������� ������� greeter � ����� greeter.proto.

����� GreeterService �� ���� ������������ ������� ����� C#. ���, �� ��������� �� ����� �����������, ������� ����������� dependency injection �������� ������ ������� � ����� ��� ������������ ��� �����������.

### ����������� gRPC
������ ����� � ��������� �� ��������� �������� ����� Program, ������� ��������� ������ � ����� Program.cs. � ������ ����� � ���������� ����������� ���� �������������� gRPC:
``` csharp
using GreeterServiceApp.Services;
 
var builder = WebApplication.CreateBuilder(args);
 
// ��������� ������� ��� ������ � gRPC
builder.Services.AddGrpc();
 
var app = builder.Build();
 
// ����������� ��������� HTTP-��������
app.MapGrpcService<GreeterService>();
app.MapGet("/", () => "Communication with gRPC endpoints must be made through a gRPC client...");
 
app.Run();
```

### ������ ��� gRPC-�������

���� ������� ����� ��������� ��������� �������:

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

#### ����������� ���� �������
����� � ������� ����������� ������� ������� ��� ����� Program.cs ��������� �������:

``` csharp
using Grpc.Net.Client;
using GreeterClientApp;
 
// ������� ����� ��� ������ ����������� � ��������
// �������� - ����� ������� gRPC
using var channel = GrpcChannel.ForAddress("http://localhost:5134");
// ������� ������
var client = new Greeter.GreeterClient(channel);
Console.Write("������� ���: ");
string? name = Console.ReadLine();
// ������������ ����������� � ��������
var reply = await client.SayHelloAsync(new HelloRequest { Name = name });
Console.WriteLine($"����� �������: {reply.Message}");
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
