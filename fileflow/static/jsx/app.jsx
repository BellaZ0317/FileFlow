/** @jsx React.DOM */

/*
var DynamicSearch = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { searchString: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
    console.log("scope updated!");
  },

  render: function() {

    var countries = this.props.items;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter countries list by value from input box
    if(searchString.length > 0){
      countries = countries.filter(function(country){
        return country.name.toLowerCase().match( searchString );
      });
    }

    return (
      <div>
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
        <ul>
          {countries.map(function(country){return <li>{country.name} })}
        </ul>
      </div>
    )
  }
});

// list of countries, defined with JavaScript object literals
const countries = [
  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
];
// TODO render search bar component with array of current files
React.render(
  <DynamicSearch items={ countries } />,
  document.getElementById('DynamicSearch')
);



var ProgressBar = React.createClass({

    getInitialState: function(){
        return { progress: "Click Here to see a worker progress",
                 task_id: 0
                };
    },

    handleClick: function(event){
        // if the state is 0, start the task
        if(this.state.task_id === 0){

            $.ajax({
              url: "react/task",
              dataType: 'json',
              success: function(data) {
                console.log(data);
                // TODO more modular way of updating this thing
                this.setState({progress: data.progress, task_id: data.task_id}, function(){
                  this.forceUpdate();
                }.bind(this));
              }.bind(this),
            });
        }else{ // we do have a task, poll for progress
            $.ajax({
              url: "react/task/"+this.state.task_id,
              dataType: 'json',
              success: function(data) {
                console.log(data);

                this.setState({progress: data.state, task_id:data.task_id}, function(){
                // console.log(this.state.data);
                this.forceUpdate();

                }.bind(this));
              }.bind(this),

             error: function(){
                 this.setState({progress: "can't connect to server, check internet connection"});
             }
           });
        }
    },

    render: function(){
        return(
            <div class='exbutton dark center' onClick={this.handleClick}>
                <p>{this.state.progress}</p>
            </div>
            )
    }

});
React.render(
    <ProgressBar/>,
    document.getElementById('ProgressBar')
);
*/

// this creates a React component that can be used in other components or
// used directly on the page with React.renderComponent
var FileForm = React.createClass({
  // since we are starting off without any data, there is no initial value
  getInitialState: function() {
    return {
      data_uri: null,
    };
  },
  // prevent form from submitting; we are going to capture the file contents
  handleSubmit: function(e) {
    e.preventDefault();
    console.log('file submitted!!');
    console.log(e);
  },
  // when a file is passed to the input field, retrieve the contents as a
  // base64-encoded data URI and save it to the component's state
  handleFile: function(e) {
    var self = this;
    var reader = new FileReader();
    var file = e.target.files[0];

    reader.onload = function(upload) {
      self.setState({
        data_uri: upload.target.result,
      })
    };
    reader.readAsDataURL(file);
  },
  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {
    // since JSX is case sensitive, be sure to use 'encType'
    return (
      <form id="create-form" onSubmit={this.handleSubmit} encType="multipart/form-data">

        <input type="number" name="space" id="reserve" placeholder="e.g. '32' "/>
        <input type="file" name="file" onChange={this.handleFile}/>

        <input id="create-button" type="submit" value="upload" class="radius button" style="font-family:Pacifico ; font-size:2em"/>
      </form>
    );
  }
});

React.render(
    <FileForm/>,
    document.getElementById('FileForm')
);
