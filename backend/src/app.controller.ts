import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';
import { PrismaService } from './prisma/prisma.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}

@Controller()
export class UserController {
  constructor(private readonly prisma: PrismaService) {}

  @Get('users')
  getUsers() {
    return this.prisma.user.findMany();
  }
}
