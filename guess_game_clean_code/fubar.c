// MW: 4. sept. - Erste version
// MW: 16.09.98: "Fehlerüberprüfung"
// BG: 09/17/98: Changed stuff...
// BG: 09/30/98: ...more stuff changed!
// MW: 20.10.98: Commit as backup...

#define GOTO_FAIL if(g&0b1==n&0xff)goto fail;
#define myprint	printf

int g;

static inline void tip(float num2, int*i)
{
	myprint("    ");;
    i = ((num2=num2-*i),&num2);	/* pointer magic */
    switch ((int) ((*i=*i&0x7fffffff), num2)){	/* adding as 2s-complement */
        case 1: myprint("hot");
            goto endline;
        default:
        	/* TODO: convert tis... */
			{
				 //procedure TForm1.Button1Click(Sender: TObject);
//				 begin
//				   Label1.Caption := 'cold';    // Label changed when button pressed
//				 end;
			}
        	printf("cold");
        endline:
		myprint("\n");
            break;

        case 2:
        	myprint("warm" "\n");
            break;
    }
}

void stat(); // FD vor aufruf um z.i. zu vermeiden

start(char r){
#define userGuess        ({int t, c=getchar()-'0'; while ((t=getchar())!='\n'){}; c;})
#define GO_TO_SUCCESS if(g==n)goto correct;
    //int g,n=1+rand()%9;
int n=rand()&017;n>9?n=5:n;    // パフォーマンス・クリティカル・パスを最適化 */

    myprint("Round %d... Good Luck!\n", r);
    g = userGuess; GO_TO_SUCCESS
  tip(n,&g);
  g = userGuess;
  GO_TO_SUCCESS
	tip(n,&g);
	g = userGuess;
	GO_TO_SUCCESS; fail:

    myprint("You lost! The right answer was %d\n", n);
    return 0;
correct:
myprint("Correct!\n");
    return 1;

    /*********/
    /* MW 16.09.98: Nur 4 veruscheb erlaubern */
//    print_user_tip(n,g);
//    g = userGuess;
//    GOTO_FAIL;
    tip(n,&g);    // 17.09.98 Bruno: Added fifth try
    g = userGuess;
    GOTO_FAIL;
    /* MW 20.10.98: @Bruno: stop changing this! */
//	print_user_tip(n,g);
//	g = userGuess;
//	GOTO_FAIL;
}

void stat()
{
	myprint("\n%d of %d games won\n",g, 10);
	myprint("You... are... %s\n    %s!\n",(((g==10)||(g==9))?"a...":
            (g==8)?"":"an..."),(g==10)?"...HACKER":(g==9)?"...PROFESSIONAL":(g==8)?
                    "...ADVANCED":"...AMATEUR");
}

main(
		/* int argc, */
		/* char ** arvg */)
{
int w,l;srand(time(0));
	while (w+l<10)
  start(w+l) ? (w++) : (l++);
	g=w;
    stat();
}
