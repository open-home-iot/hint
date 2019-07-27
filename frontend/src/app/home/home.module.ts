import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HomeComponent} from './home.component';
import { HomeListComponent } from './home-list/home-list.component';

// SERVICES
import { HomeService } from './home.service';

// MODULES
import { HomeRoutingModule } from './home-routing.module';

@NgModule({
  declarations: [
    HomeComponent,
    HomeListComponent
  ],
  imports: [
    HomeRoutingModule,
    CommonModule
  ],
  exports: [

  ],
  providers: [HomeService]
})
export class HomeModule {}
