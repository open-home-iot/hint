import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { UserOverviewComponent } from './pages/user-overview/user-overview.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { UserListComponent } from './user-list/user-list.component';

// SERVICES
import { UserService } from './user.service';

// MODULES
import { UserRoutingModule } from './user-routing.module';

@NgModule({
  declarations: [
    UserOverviewComponent,
    UserDetailComponent,
    UserListComponent
  ],
  imports: [
    UserRoutingModule,
    CommonModule
  ],
  exports: [

  ],
  providers: [UserService]
})
export class UserModule {}
