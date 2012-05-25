%%%%%
% coin_count
%
% Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
%
% This is free software; you can redistribute it and/or modify it
% under the terms of the GNU Lesser General Public License as
% published by the Free Software Foundation; either version 2.1 of
% the License, or (at your option) any later version.
%
% This software is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
% Lesser General Public License for more details.
%
% You should have received a copy of the GNU Lesser General Public
% License along with this software; if not, write to the Free
% Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
% 02110-1301 USA, or see the FSF site: http://www.fsf.org.
%%%%%

clear;
clf;

%%
colormap('Gray');

% NOTIZ: Bild wurde von Hand veraendert, sodass zwei Muenzen auch als
% verschiedene erkannt werden!
Irgb=imread('IMAG0092_improved.jpg');

subplot(2,4,1);
imagesc(Irgb)
title('1. original');

%%
Ibw=rgb2gray(Irgb);

subplot(2,4,2);
imagesc(Ibw)
title('2. grayscale');

%%

% erodieren
SE=ones(3,3);

Itemp=imerode(Ibw,SE);
Itemp=imerode(Itemp,SE);

subplot(2,4,3);
imagesc(Itemp)
title('3. erode');

%%

% finde kanten per canny filter
% TODO: sollte vielleicht durch ein einfaches 2-Pegel-Bild ersetzt werden
Itemp=edge(Itemp,'canny',0.03);

subplot(2,4,4);
imagesc(Itemp)
title('4. canny');

%%

% dilatation
Itemp=imdilate(Itemp,SE);
Itemp=imdilate(Itemp,SE);

subplot(2,4,5);
imagesc(Itemp)
title('5. dilate');

%%
subplot(2,4,6);

% Suche im Bild Objekte
L=bwlabel(Itemp);

% Faerbe die gefundenen Objekte zufaellig ein
col=label2rgb(L,'jet','w','shuffle');

imagesc(col); 
title('6. bwlabel');

%%
% TODO: Das Attribut sollte frei waehlbar sein...

% hole alle benoetigten Attribute zu den Objekten
props=regionprops(L,'Area','Centroid','Perimeter','MajorAxisLength');

% schreibe die einzelnen Attribute in ein Vektor um einfacherer arbeiten zu
% können.
area=[props.Area];
axis=[props.MajorAxisLength];
cent=[props.Centroid];
perm=[props.Perimeter];

% Beide props koennten verwendet werden. Ich brauch aber erstmal nur eins...
ObjArea=find(area > 10000); % Muenzen-Groeße anscheinend ueber 60000
ObjAxis=find(axis > 100); % Muenzen-Axis-Lenght anscheinend etwa 300 bis 900

% Waehle nur Objekte aus, die auch den Kriterien entsprechen
mask=ismember(L, ObjArea);

subplot(2,4,7);
imagesc(mask);

title('7. ismember');


%%
% TODO: hier sollte keine referenz auf area() sein, damit man das attribut
% im Schritt vorher frei waehlen kann...

subplot(2,4,8);
imagesc(mask);

title('8. coins');

summe = 0;

for i = ObjArea
    [r, c] = find(L==i);
    
    % Ermittelte Werte fuer Muenzen: 
    % 60746 68729 74255 85665 90274 97696 130403
    % suche den text der in das bild fuer dieses Objekt geschrieben werden
    % soll
    if ((area(i) >= 55000) && (area(i) <= 65000))
        z = 1;
    elseif ((area(i) >= 65001) && (area(i) <= 70000))
        z = 5;
    elseif ((area(i) >= 70001) && (area(i) <= 75000))
        z = 2;
    elseif ((area(i) >= 75001) && (area(i) <= 87000))
        z = 10;
    elseif ((area(i) >= 87001) && (area(i) <= 95000))
        z = 100;
    elseif ((area(i) >= 95001) && (area(i) <= 100000))
        z = 20;
    elseif ((area(i) >= 100001) && (area(i) <= 200000))
        z = 50;
    else
        z = 0;
    end
    
    summe = summe + z;
    cointext = strcat(num2str(z), ' c');
    
    % zeichne vorher ausgewaehlten text in bild an stelle des ersten
    % gefundenen Pixels
    text(c(1),r(1),cointext,'Color',[1,1,1], 'BackgroundColor',[0,0,0], 'FontSize',12);
end

sumtext = strcat('summe: ', num2str(summe), ' c');
text(200,200,sumtext,'Color',[1,1,1], 'BackgroundColor',[0,0,0], 'FontSize',12);














