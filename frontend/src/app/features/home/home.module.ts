import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HomeListComponent } from './home-list/home-list.component';
import { HomeDetailComponent } from './home-detail/home-detail.component';
import { HomeOverviewComponent } from './pages/home-overview/home-overview.component';

// SERVICES
import { HomeService } from './home.service';

// MODULES
import { HomeRoutingModule } from './home-routing.module';

@NgModule({
  declarations: [
    HomeListComponent,
    HomeDetailComponent,
    HomeOverviewComponent
  ],
  imports: [
    HomeRoutingModule,
    CommonModule
  ],
  exports: [
    HomeOverviewComponent
  ],
  providers: [HomeService]
})
export class HomeModule {}
