#### Just a place to sketch out structure of code.

* [Scheduled Task](DynamicTaskViewerDemo/Schedules/__init__.py) Object
  - *def* **update_parameter**  
    - used to inject a new parameter to Task Object, clearing storage if necessary.
    
  - *async* **run_task**
    - protocol used by [Main UI](DynamicTaskViewerDemo/MainUI.py) to provide executable coroutine.
    
    
