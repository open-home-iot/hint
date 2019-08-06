import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { EventOverviewComponent } from './pages/event-overview/event-overview.component';

// SERVICES
import { EventService } from './event.service';

// MODULES
import { EventRoutingModule } from './event-routing.module';
import { EventIconsComponent } from './event-icons/event-icons.component';

@NgModule({
  declarations: [
    EventOverviewComponent,
    EventIconsComponent
  ],
  imports: [
    EventRoutingModule,
    CommonModule
  ],
  exports: [
    EventOverviewComponent,
  ],
  providers: [EventService]
})
export class EventModule {}
