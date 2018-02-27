
//Globals
var currentTextInput;
var puzzelArrayData;
//Loads the Crossword
function initializeScreen(){
	var puzzelTable = document.getElementById("puzzel");
	puzzelArrayData = preparePuzzelArray();
	for ( var i = 0; i < puzzelArrayData.length ; i++ ) {
		var row = puzzelTable.insertRow(-1);
		var rowData = puzzelArrayData[i];
		for(var j = 0 ; j < rowData.length ; j++){
			var cell = row.insertCell(-1);
			if(rowData[j] != 0){
				var txtID = String('txt' + '_' + i + '_' + j);
				cell.innerHTML = '<input type="text" class="inputBox" maxlength="1" style="text-transform: lowercase" ' + 'id="' + txtID + '" onfocus="textInputFocus(' + "'" + txtID + "'"+ ')">';
			}else{
				cell.style.backgroundColor  = "black";
			}
		}
	}
	addHint();
}
//Adds the hint numbers
function addHint(){
	document.getElementById("txt_0_3").placeholder = "1";
	document.getElementById("txt_2_2").placeholder = "2";
	document.getElementById("txt_3_0").placeholder = "3";
	document.getElementById("txt_4_0").placeholder = "4";
	document.getElementById("txt_6_5").placeholder = "5";
	document.getElementById("txt_7_0").placeholder = "6";
	document.getElementById("txt_7_2").placeholder = "7";
	document.getElementById("txt_10_1").placeholder = "8";
	// document.getElementById("txt_7_2").placeholder = "7";
}
//Stores ID of the selected cell into currentTextInput
function textInputFocus(txtID123){
	currentTextInput = txtID123;
}
//Returns Array
function preparePuzzelArray(){
// 	var items = [	[0, 'д', 'о', 'м', 0, 0, 0, 0],
// 	[0, 0, 'х', 0, 0, 0, 0, 0],
// 	[0, 0, 'р', 0, 0, 0, 0, 'к'],
// 	[0, 'б', 'а', 'д', 'м', 0, 0, 'и'],
// 	[0, 0, 'н', 0, 0, 0, 0, 'р'],
// 	['п', 'р', 'а', 'к', 'т', 'и', 'к', 'а']
// ];

var items = [
[0,0,0,'п',0,0,0],
[0,0,0,'р',0,0,0],
[0,0,'б','а','д','м',0],
['с',0,0,'к',0,0,0],
['а','р','к','т','и','к','а'],
['м',0,0,'и',0,0,0],
['б',0,0,'к',0,'т',0],
['о','х','р','а','н','а',0],
[0,0,'а',0,0,'к',0],
[0,0,'д',0,0,'т',0],
[0,'з','о','н','т','и','к'],
[0,0,'с',0,0,'к',0],
[0,0,'т',0,0,'а',0],
[0,0,'ь',0,0,0,0]
];

return items;
}
//Clear All Button
function clearAllClicked(){
	currentTextInput = '';
	var puzzelTable = document.getElementById("puzzel");
	puzzelTable.innerHTML = '';
	document.getElementById("agentx").src="resources/img/lk.png";
	document.getElementById("greetings").src = "";
	document.getElementById("greetings").style.display = "none";
	document.getElementById("kira").src = "";
	document.getElementById("kira").style.display = "none";
	document.getElementById("videosms1").style.display = "none";
	document.getElementById("videosms2").style.display = "none";
	initializeScreen();
}
//Check button
function checkClicked(){
	for ( var i = 0; i < puzzelArrayData.length ; i++ ) {
		var rowData = puzzelArrayData[i];
		var yes=1;
		for(var j = 0 ; j < rowData.length ; j++){
			if(rowData[j] != 0){
				var selectedInputTextElement = document.getElementById('txt' + '_' + i + '_' + j);
				if(selectedInputTextElement.value != puzzelArrayData[i][j]){
					selectedInputTextElement.style.backgroundColor = 'red';
					document.getElementById("agentx").src="resources/img/lk.png";
					document.getElementById("greetings").src = "";
					document.getElementById("greetings").style.display = "none";
					document.getElementById("kira").src = "";
					document.getElementById("kira").style.display = "none";
					document.getElementById("videosms1").style.display = "none";
					document.getElementById("videosms2").style.display = "none";
					yes=0

				}else{
					selectedInputTextElement.style.backgroundColor = 'white'
				}
			}
		}
		if (yes===1){
			document.getElementById("greetings").src = "https://www.youtube.com/embed/h7tEeLCPFHE";
			document.getElementById("kira").src = "https://www.youtube.com/embed/V5eTbBVlVRw";
			document.getElementById("agentx").src="resources/img/unlk.png";
			document.getElementById("kira").style.display = "inline";
			document.getElementById("greetings").style.display = "inline";

			document.getElementById("videosms1").style.display = "inline";
			document.getElementById("videosms2").style.display = "inline";

		}
	}
}
//Clue Button
function clueClicked(){
	if (currentTextInput != null){
		var temp1 = currentTextInput;
		var token = temp1.split("_");
		var row = token[1];
		var column = token[2];
		document.getElementById(temp1).value = puzzelArrayData[row][column];
		//checkClicked();
	}
}
//Solve Button
function solveClicked(){
	if (currentTextInput != null){
		var temp1 = currentTextInput;
		var token = temp1.split("_");
		var row = token[1];
		var column = token[2];

		// Print elements on top
		for(j = row; j >= 0; j--){
			if(puzzelArrayData[j][column] != 0){
				document.getElementById('txt' + '_' + j + '_' + column).value = puzzelArrayData[j][column];
			}else break;
		}
		// Print elements on right
		for(i = column; i< puzzelArrayData[row].length; i++){
			if(puzzelArrayData[row][i] != 0){
				document.getElementById('txt' + '_' + row + '_' + i).value = puzzelArrayData[row][i];
			}else break;
		}

		// Print elements below
		for(m = row; m< puzzelArrayData.length; m++){
			if(puzzelArrayData[m][column] != 0){
				document.getElementById('txt' + '_' + m + '_' + column).value = puzzelArrayData[m][column];
			}else break;
		}
		// Print elements on left
		for(k = column; k >= 0; k--){
			if(puzzelArrayData[row][k] != 0){
				document.getElementById('txt' + '_' + row + '_' + k).value = puzzelArrayData[row][k];
			}else break;
		}
		// Done!

	}
}
