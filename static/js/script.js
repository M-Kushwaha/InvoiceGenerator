console.log("SCRIPT LOADED");
document.addEventListener('DOMContentLoaded', () => {
	
//UI REFERENCES
    const gst=document.getElementById("gsttax");
	const tableBody = document.getElementById('productbody');
	let grandtotal = document.getElementById("grandtotal");
	const addRow = document.getElementById("addrowbtn")
	let subTotalVal = document.getElementById("subtotal");
	
	
	
//DOM LISTENERES
	addRow.addEventListener("click", addrow);
	tableBody.addEventListener("input", calculateLineTotal);
	tableBody.addEventListener("click", deleteRow);
	gst.addEventListener("input", calculateGrandtotal);
	
	
//UTILITY function
	function runningSum(arrayInput) {
			let subtotal=0;
			for (let i = 0; i < arrayInput.length; i++) {
			let val = arrayInput[i].value;
			let a=parseFloat(val);
			if (a !== a) {a=0;}
            subtotal += a;
            }
		return subtotal;
		}	
	
	
	
//BUSINESS LOGIC
	function addrow() {
        const tr = document.createElement('tr');
		tr.innerHTML=`
        <td> <input type="text"	name="product_name[]" size="50" required/> </td>
		<td> <input type="number" name="quantity[]" min="1" required/> </td>
		<td> <input type="number" name="rate[]"  min="0" step="0.01" required/></td>
		<td> <input type="number" name="line_total[]" readonly/></td>
		<td> <button type="button" class="deleterowbtn"> <abbr title="Delete Row">X</abbr></button> </td>`;
        document.getElementById('productbody').appendChild(tr);
        }
		
		
	
//calculate line total by multiplying quantity and ratw	
	function calculateLineTotal(event) {
		if(event.target.getAttribute("name") === 'quantity[]' || event.target.getAttribute("name") === 'rate[]') { //if triggered event is associated with tagname quantity or rate, proceed with the following..
		const elmnt= event.target;  		//store the actual element (quantity or rate)

		const temp = elmnt.closest("tr");
		
		//convert the quantity, rate and total inputs to integers.
		let qtyInput = temp.querySelector('input[name="quantity[]"]');
		let rateInput = temp.querySelector('input[name="rate[]"]');
		let totalInput = temp.querySelector('input[name="line_total[]"]');
		
		let qtyVal = parseFloat (qtyInput.value);
		let rateVal = parseFloat (rateInput.value);
		//let totalVal= temp.querySelector('input[name="line_total[]"]');
		
		qtyVal = qtyVal? qtyVal : 0;   //if values falsey -> convert to zero.
		rateVal = rateVal? rateVal : 0;
		let lineTotal = qtyVal * rateVal;
		
		totalInput.value = lineTotal;
		calculateSubtotal();
		calculateGrandtotal();
		}}
		
	

//Subtotal calculation	
	function calculateSubtotal() {
		const allRowTotals = document.getElementsByName('line_total[]');
		let totalSum = runningSum(allRowTotals);
		subTotalVal.value = totalSum;
		}	
		
		
		
//Delete row 		
	function deleteRow(event) {
		if(event.target.closest(".deleterowbtn") ) { //if click event's ancestor class is deleterowbtn -> proceed with the following..
		
		const row = event.target.closest("tr");		//get the closest tr ancestor of the element
		//count the number of rows in tbody
		let noOfRows = tableBody.childElementCount;
		
		if (noOfRows > 1) {
			row.remove();
			calculateSubtotal();
			calculateGrandtotal();
		}}}



//GST calculation
	function calculateGrandtotal() {		
		let subtotal = parseFloat (document.getElementById("subtotal").value) || 0;
		let gstVal = parseFloat (document.getElementById("gsttax").value) || 0;	
		let gstAmount = subtotal * (gstVal/100);
			
		grandtotal.value = subtotal+gstAmount;	}

			
});

	

	
	