from django.contrib.auth.models import User, Group

Group.objects.create(name='admin')
Group.objects.create(name='compras')
Group.objects.create(name='vendas')
Group.objects.create(name='stock')
Group.objects.create(name='producao')

admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
admin.groups.add(Group.objects.get(name='admin'))
admin.save()

compras = User.objects.create_user('compras', 'compras@compras.com', 'compras')
compras.groups.add(Group.objects.get(name='compras'))
compras.save()

vendas = User.objects.create_user('vendas', 'vendas@vendas.com', 'vendas')
vendas.groups.add(Group.objects.get(name='vendas'))
vendas.save()

stock = User.objects.create_user('stock', 'stock@stock.com', 'stock')
stock.groups.add(Group.objects.get(name='stock'))
stock.save()

producao = User.objects.create_user('producao', 'producao@producao.com', 'producao')
producao.groups.add(Group.objects.get(name='producao'))
producao.save()